# Google ADK Weather API

A voice-enabled weather API using Google Cloud Speech-to-Text and OpenWeatherMap API. Built as part of Miami Dade College CAI2840C coursework.

## Features

- 🎤 **Speech-to-Text**: Convert voice queries to text using Google Cloud Speech-to-Text API
- 🌤️ **Weather Data**: Real-time weather information using OpenWeatherMap API
- 💾 **Firestore Logging**: Store query history in Google Cloud Firestore
- 🚀 **Cloud Run Ready**: Deployable to Google Cloud Run
- 🔌 **REST API**: Multiple endpoints for text, audio, and direct city queries

## Architecture

```
Audio Input → Speech-to-Text → City Extraction → Weather API → Firestore → JSON Response
```

## Prerequisites

1. **Google Cloud Account** with the following APIs enabled:
   - Speech-to-Text API
   - Firestore API
   - Cloud Run API

2. **OpenWeatherMap API Key** (free tier available)
   - Sign up at: https://openweathermap.org/api

3. **Python 3.11+**

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/nduarte215/Google-ADK-Weather-API.git
cd Google-ADK-Weather-API
```

### Step 2: Set Up Google Cloud

1. **Create a Google Cloud Project** (if you haven't already)
   ```bash
   gcloud projects create your-project-id
   gcloud config set project your-project-id
   ```

2. **Enable Required APIs**
   ```bash
   gcloud services enable speech.googleapis.com
   gcloud services enable firestore.googleapis.com
   gcloud services enable run.googleapis.com
   ```

3. **Create a Firestore Database**
   ```bash
   gcloud firestore databases create --region=us-east1
   ```

4. **Set Up Authentication**
   ```bash
   gcloud auth application-default login
   ```

### Step 3: Get OpenWeatherMap API Key

1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key

### Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```bash
   OPENWEATHER_API_KEY=your_actual_api_key_here
   GOOGLE_CLOUD_PROJECT=your-project-id
   ```

### Step 5: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 6: Run Locally

```bash
# Export environment variables (on Mac/Linux)
export OPENWEATHER_API_KEY="your_api_key"
export GOOGLE_CLOUD_PROJECT="your-project-id"

# On Windows PowerShell:
# $env:OPENWEATHER_API_KEY="your_api_key"
# $env:GOOGLE_CLOUD_PROJECT="your-project-id"

# Run the Flask app
python app.py
```

The API will be available at `http://localhost:8080`

## API Endpoints

### 1. Health Check
```bash
GET /
```

### 2. Weather from Text Query
```bash
POST /weather/text
Content-Type: application/json

{
  "query": "What's the weather in Miami"
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:8080/weather/text \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in Miami"}'
```

### 3. Weather from Audio File
```bash
POST /weather/audio
Content-Type: multipart/form-data

Form field: audio (audio file in WAV format)
```

**Example using curl:**
```bash
curl -X POST http://localhost:8080/weather/audio \
  -F "audio=@weather_query.wav"
```

### 4. Weather by City Name
```bash
GET /weather/{city}
```

**Example:**
```bash
curl http://localhost:8080/weather/Miami
```

### 5. Query History
```bash
GET /history
```

Returns the last 10 weather queries from Firestore.

## Testing the Application

### Test with Text Query

```bash
# Using curl
curl -X POST http://localhost:8080/weather/text \
  -H "Content-Type: application/json" \
  -d '{"query": "weather in New York"}'
```

### Test with Direct City Query

```bash
curl http://localhost:8080/weather/Miami
```

### Test with Audio (requires .wav file)

First, create a simple test audio file or use your phone to record "What's the weather in Miami?" and convert to WAV format.

```bash
curl -X POST http://localhost:8080/weather/audio \
  -F "audio=@test_query.wav"
```

## Deploying to Google Cloud Run

### Step 1: Build and Push Docker Image

```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Build the container
gcloud builds submit --tag gcr.io/$PROJECT_ID/weather-api

# Or use Docker directly:
# docker build -t gcr.io/$PROJECT_ID/weather-api .
# docker push gcr.io/$PROJECT_ID/weather-api
```

### Step 2: Deploy to Cloud Run

```bash
gcloud run deploy weather-api \
  --image gcr.io/$PROJECT_ID/weather-api \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated \
  --set-env-vars OPENWEATHER_API_KEY=your_api_key,GOOGLE_CLOUD_PROJECT=$PROJECT_ID
```

### Step 3: Get Your Service URL

After deployment, Cloud Run will provide a URL like:
```
https://weather-api-xxxxxxxxxx-ue.a.run.app
```

Test it:
```bash
curl https://your-cloud-run-url/weather/Miami
```

## Example Response

```json
{
  "city": "Miami",
  "weather": {
    "city": "Miami",
    "temperature": 78.5,
    "feels_like": 82.1,
    "humidity": 75,
    "description": "partly cloudy",
    "wind_speed": 8.5,
    "timestamp": "2025-12-09T14:30:00"
  },
  "response_text": "The weather in Miami is currently 78.5°F with partly cloudy. It feels like 82.1°F. Humidity is at 75% with wind speeds of 8.5 mph."
}
```

## Project Structure

```
Google-ADK-Weather-API/
├── app.py                  # Flask API application
├── weather_agent.py        # Core weather agent logic
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── .env.example           # Environment template
├── README.md             # This file
└── tests/                # Test files (optional)
```

## Troubleshooting

### "OPENWEATHER_API_KEY not set" Error

Make sure you've set the environment variable:
```bash
export OPENWEATHER_API_KEY="your_key_here"
```

### "Could not initialize Firestore" Error

1. Verify Firestore is enabled in your Google Cloud project
2. Check that you've authenticated with: `gcloud auth application-default login`
3. Verify your GOOGLE_CLOUD_PROJECT environment variable is set

### Speech-to-Text API Errors

1. Ensure Speech-to-Text API is enabled in your project
2. Check that your audio file is in a supported format (WAV, FLAC)
3. Audio should be 16kHz sample rate for best results

### Import Errors

Make sure you're in your virtual environment and have installed all requirements:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Course Assignment Notes

This project demonstrates:
- ✅ Google Cloud Speech-to-Text API integration
- ✅ External API integration (OpenWeatherMap)
- ✅ Google Cloud Firestore for data persistence
- ✅ RESTful API design with Flask
- ✅ Cloud Run deployment
- ✅ Error handling and logging

## License

MIT License - see LICENSE file for details

## Author

Nasley Duarte - Miami Dade College CAI2840C

## Resources

- [Google Cloud Speech-to-Text Documentation](https://cloud.google.com/speech-to-text/docs)
- [OpenWeatherMap API Documentation](https://openweathermap.org/api)
- [Google Cloud Firestore Documentation](https://cloud.google.com/firestore/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
