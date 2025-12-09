#!/bin/bash

# Google ADK Weather API - Cloud Run Deployment Script
# This script automates the deployment process

set -e  # Exit on error

echo "======================================================"
echo "GOOGLE ADK WEATHER API - CLOUD RUN DEPLOYMENT"
echo "======================================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI not found"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No project set"
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo ""
echo "📋 Project: $PROJECT_ID"
echo ""

# Get OpenWeather API key
if [ -z "$OPENWEATHER_API_KEY" ]; then
    echo "⚠️  OPENWEATHER_API_KEY not set"
    read -p "Enter your OpenWeather API key: " OPENWEATHER_API_KEY
fi

# Confirm deployment
echo ""
echo "This will:"
echo "  1. Build Docker container"
echo "  2. Push to Google Container Registry"
echo "  3. Deploy to Cloud Run (us-east1)"
echo ""
read -p "Continue? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

# Step 1: Enable required APIs
echo ""
echo "📡 Enabling required APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    speech.googleapis.com \
    firestore.googleapis.com

# Step 2: Build container
echo ""
echo "🔨 Building container..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/weather-api

# Step 3: Deploy to Cloud Run
echo ""
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy weather-api \
    --image gcr.io/$PROJECT_ID/weather-api \
    --platform managed \
    --region us-east1 \
    --allow-unauthenticated \
    --set-env-vars OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY,GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
    --memory 512Mi \
    --timeout 60

# Get service URL
echo ""
echo "✅ Deployment complete!"
echo ""
SERVICE_URL=$(gcloud run services describe weather-api --region us-east1 --format 'value(status.url)')

echo "======================================================"
echo "YOUR API IS LIVE!"
echo "======================================================"
echo ""
echo "Service URL: $SERVICE_URL"
echo ""
echo "Test your API:"
echo "  curl $SERVICE_URL/weather/Miami"
echo ""
echo "Or with text query:"
echo "  curl -X POST $SERVICE_URL/weather/text \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"query\": \"weather in New York\"}'"
echo ""
echo "======================================================"
