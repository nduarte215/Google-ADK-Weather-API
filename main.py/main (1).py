from flask import Flask, request, jsonify
import os
from google.cloud import speech_v1
from google.cloud import firestore
import requests
from datetime import datetime

app = Flask(__name__)

# Initialize Firestore client
db = firestore.Client()

# OpenWeatherMap API configuration
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

def transcribe_audio(audio_content):
    """Transcribe audio using Google Speech-to-Text API"""
    client = speech_v1.SpeechClient()
    
    audio = speech_v1.RecognitionAudio(content=audio_content)
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    
    response = client.recognize(config=config, audio=audio)
    
    # Get the first result
    if response.results:
        return response.results[0].alternatives[0].transcript
    return None

def get_weather(city):
    """Get weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'imperial'  # For Fahrenheit
        }
        
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        weather_info = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed']
        }
        
        return weather_info
    except Exception as e:
        return {'error': str(e)}

def extract_city_from_text(text):
    """Extract city name from transcribed text"""
    # Simple extraction - looks for common patterns
    text_lower = text.lower()
    
    # Remove common weather query words
    words_to_remove = ['weather', 'in', 'what', 'is', 'the', 'whats', "what's", 
                       'tell', 'me', 'about', 'for', 'how', 'temperature']
    
    words = text.split()
    city_words = [word for word in words if word.lower() not in words_to_remove]
    
    # Join remaining words as city name
    city = ' '.join(city_words).strip()
    
    # Default to Miami if no city detected
    if not city:
        city = "Miami"
    
    return city

def save_to_firestore(request_data, weather_data):
    """Save request and response to Firestore"""
    try:
        doc_ref = db.collection('weather_requests').document()
        doc_ref.set({
            'timestamp': datetime.now(),
            'transcript': request_data.get('transcript', ''),
            'city': request_data.get('city', ''),
            'weather': weather_data,
            'method': request_data.get('method', 'text')
        })
    except Exception as e:
        print(f"Error saving to Firestore: {e}")

@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        'service': 'ADK Weather API',
        'version': '1.0',
        'endpoints': {
            '/weather/text': 'GET - Query weather by city name',
            '/weather/speech': 'POST - Query weather using voice (audio file)',
            '/health': 'GET - Health check'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/weather/text', methods=['GET'])
def weather_text():
    """Get weather by city name (text query)"""
    city = request.args.get('city', 'Miami')
    
    # Get weather data
    weather_data = get_weather(city)
    
    # Save to Firestore
    request_data = {
        'transcript': f"Weather query for {city}",
        'city': city,
        'method': 'text'
    }
    save_to_firestore(request_data, weather_data)
    
    return jsonify({
        'success': True,
        'city': city,
        'weather': weather_data
    })

@app.route('/weather/speech', methods=['POST'])
def weather_speech():
    """Get weather using voice input"""
    try:
        # Check if audio file is provided
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        audio_content = audio_file.read()
        
        # Transcribe audio
        transcript = transcribe_audio(audio_content)
        
        if not transcript:
            return jsonify({'error': 'Could not transcribe audio'}), 400
        
        # Extract city from transcript
        city = extract_city_from_text(transcript)
        
        # Get weather data
        weather_data = get_weather(city)
        
        # Save to Firestore
        request_data = {
            'transcript': transcript,
            'city': city,
            'method': 'speech'
        }
        save_to_firestore(request_data, weather_data)
        
        return jsonify({
            'success': True,
            'transcript': transcript,
            'city': city,
            'weather': weather_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get weather query history from Firestore"""
    try:
        limit = int(request.args.get('limit', 10))
        
        # Query Firestore for recent requests
        docs = db.collection('weather_requests').order_by(
            'timestamp', direction=firestore.Query.DESCENDING
        ).limit(limit).stream()
        
        history = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            # Convert timestamp to string for JSON serialization
            if 'timestamp' in data:
                data['timestamp'] = data['timestamp'].isoformat()
            history.append(data)
        
        return jsonify({
            'success': True,
            'count': len(history),
            'history': history
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
