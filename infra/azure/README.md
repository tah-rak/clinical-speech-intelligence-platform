# Azure AI Speech Setup Guide

## 1. Create Azure Speech Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new **Speech** resource
3. Select your subscription, resource group, and region (e.g., `eastus`)
4. Choose pricing tier (Free F0 tier available for testing)

## 2. Get Credentials

After deployment:
- Copy **Key 1** from Keys and Endpoint
- Note the **Region** (e.g., `eastus`)

## 3. Install Optional Dependency

```bash
pip install azure-cognitiveservices-speech
```

## 4. Configure Environment

```env
STT_PROVIDER=azure
AZURE_SPEECH_ENABLED=true
AZURE_SPEECH_KEY=your-speech-key
AZURE_SPEECH_REGION=eastus
```

## 5. Fallback Behavior

If Azure credentials are missing or invalid, the platform automatically falls back to local faster-whisper transcription.
