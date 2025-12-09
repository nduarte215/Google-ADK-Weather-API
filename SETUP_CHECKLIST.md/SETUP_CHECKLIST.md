# ADK Weather API - Setup Checklist

Print this page and check off each step as you complete it!

## Pre-Deployment Checklist

### Part 1: Prerequisites (10 minutes)

- [ ] **Google Cloud Account**
  - Go to https://cloud.google.com
  - Sign up or log in
  - Enable billing (required for deployment)
  
- [ ] **Python 3.11+ Installed**
  - Check version: `python --version`
  - Download from: https://www.python.org/downloads/
  
- [ ] **Git Installed**
  - Check: `git --version`
  - Download from: https://git-scm.com/downloads/
  
- [ ] **Google Cloud SDK Installed**
  - Check: `gcloud --version`
  - Download from: https://cloud.google.com/sdk/docs/install
  - Run: `gcloud init`

### Part 2: API Keys (5 minutes)

- [ ] **OpenWeatherMap API Key**
  - Visit: https://openweathermap.org/api
  - Sign up for free account
  - Navigate to: https://home.openweathermap.org/api_keys
  - Copy your API key
  - Save it somewhere safe: _______________________________

### Part 3: Google Cloud Setup (10 minutes)

- [ ] **Login to Google Cloud**
  ```bash
  gcloud auth login
  ```

- [ ] **Create or Select Project**
  ```bash
  # Create new:
  gcloud projects create adk-weather-api-xxxx
  # Or list existing:
  gcloud projects list
  ```
  
- [ ] **Set Active Project**
  ```bash
  gcloud config set project YOUR_PROJECT_ID
  ```
  Project ID: _______________________________

- [ ] **Enable Billing**
  - Go to: https://console.cloud.google.com/billing
  - Link billing account to project
  - ✅ Billing enabled

- [ ] **Enable Required APIs**
  ```bash
  gcloud services enable run.googleapis.com
  gcloud services enable speech.googleapis.com
  gcloud services enable firestore.googleapis.com
  gcloud services enable cloudbuild.googleapis.com
  ```

- [ ] **Create Firestore Database**
  ```bash
  gcloud firestore databases create --location=us-east1
  ```

## Deployment Checklist

### Option A: Automated Deployment (Recommended)

- [ ] **Download Project Files**
  - Download all files from outputs
  - Extract to folder: adk-weather-api/

- [ ] **Open Terminal in Project Folder**
  ```bash
  cd path/to/adk-weather-api
  ```

- [ ] **Make Deploy Script Executable** (Mac/Linux only)
  ```bash
  chmod +x deploy.sh
  ```

- [ ] **Run Deployment Script**
  ```bash
  ./deploy.sh
  ```
  - Enter your Project ID
  - Enter your Weather API Key
  - Confirm deployment

- [ ] **Save Service URL**
  - Copy the URL shown after deployment
  - Service URL: _______________________________

### Option B: Manual Deployment

- [ ] **Download Project Files**
- [ ] **Navigate to Project Folder**
- [ ] **Deploy to Cloud Run**
  ```bash
  gcloud run deploy adk-weather-api \
    --source . \
    --platform managed \
    --region us-east1 \
    --allow-unauthenticated \
    --set-env-vars WEATHER_API_KEY="YOUR_API_KEY"
  ```
- [ ] **Get Service URL**
  ```bash
  gcloud run services describe adk-weather-api \
    --region us-east1 \
    --format='value(status.url)'
  ```

## Testing Checklist

- [ ] **Test Health Endpoint**
  ```bash
  curl YOUR_SERVICE_URL/health
  ```
  Expected: {"status": "healthy", ...}

- [ ] **Test Weather Endpoint - Miami**
  ```bash
  curl "YOUR_SERVICE_URL/weather/text?city=Miami"
  ```
  Expected: Weather data for Miami

- [ ] **Test Weather Endpoint - Different City**
  ```bash
  curl "YOUR_SERVICE_URL/weather/text?city=NewYork"
  ```
  Expected: Weather data for New York

- [ ] **Test History Endpoint**
  ```bash
  curl "YOUR_SERVICE_URL/history?limit=5"
  ```
  Expected: List of recent queries

- [ ] **Check Firestore Data**
  - Open: https://console.cloud.google.com/firestore
  - Navigate to: weather_requests collection
  - Verify: Query data is being stored

## Local Testing Checklist (Optional)

- [ ] **Create Virtual Environment**
  ```bash
  python -m venv venv
  ```

- [ ] **Activate Virtual Environment**
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`

- [ ] **Install Dependencies**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Set Environment Variable**
  - Windows PowerShell: `$env:WEATHER_API_KEY="your_key"`
  - Windows CMD: `set WEATHER_API_KEY=your_key`
  - Mac/Linux: `export WEATHER_API_KEY="your_key"`

- [ ] **Run Application**
  ```bash
  python main.py
  ```

- [ ] **Test Locally**
  - Open browser: http://localhost:8080
  - Test endpoint: http://localhost:8080/weather/text?city=Miami

- [ ] **Run Test Client**
  ```bash
  python test_client.py
  ```

## Documentation Checklist

- [ ] **Take Screenshots**
  - [ ] Cloud Run deployment success page
  - [ ] Health check response
  - [ ] Weather query response
  - [ ] Firestore database with data
  - [ ] Service URL in browser

- [ ] **Update GitHub Repository**
  - [ ] Upload all project files
  - [ ] Commit changes
  - [ ] Push to GitHub
  - [ ] Verify files are visible

- [ ] **Document Your Work**
  - [ ] Write brief project description
  - [ ] List technologies used
  - [ ] Explain challenges and solutions
  - [ ] Include example API calls

## Submission Checklist

- [ ] **GitHub Repository Link**
  - Repository URL: _______________________________

- [ ] **Deployed Service URL**
  - Service URL: _______________________________

- [ ] **Screenshots Folder**
  - [ ] Deployment success
  - [ ] API responses
  - [ ] Firestore data

- [ ] **Project Documentation**
  - [ ] How it works explanation
  - [ ] Architecture description
  - [ ] API endpoint documentation

- [ ] **Testing Evidence**
  - [ ] Test results
  - [ ] Example requests/responses

## Troubleshooting Completed

If you encountered issues, document:
- [ ] Problem: _______________________________
- [ ] Solution: _______________________________

- [ ] Problem: _______________________________
- [ ] Solution: _______________________________

## Final Verification

- [ ] All endpoints work correctly
- [ ] Data is stored in Firestore
- [ ] GitHub repository is complete
- [ ] Documentation is clear
- [ ] Screenshots are captured
- [ ] Project is ready for submission

## Time Tracking

Started: ________ Completed: ________ Total Time: ________

## Notes & Observations

_______________________________________________________
_______________________________________________________
_______________________________________________________
_______________________________________________________

---

✅ **Checklist Complete!** Your ADK Weather API is ready!

**Remember to delete your Cloud Run service after grading to avoid charges:**
```bash
gcloud run services delete adk-weather-api --region us-east1
```
