# Sample Data

This folder contains sample clinical conversation data for demo and evaluation.

## Files

- `sample_transcript.txt` — Mock doctor-patient conversation (use with "sample transcript" upload option)
- `reference_transcript.txt` — Reference transcript for WER evaluation
- `mock_entities.json` — Example entity extraction output
- `mock_soap_note.json` — Example SOAP note output

## Adding Your Own Audio

1. Record or obtain a `.wav`, `.mp3`, or `.m4a` clinical conversation (ensure you have consent for demo use).
2. Upload via the **Upload Visit** page in the application.
3. Click **Upload and Process** to run the full pipeline.

## Demo Without Audio

Use the **Use sample transcript** checkbox on the Upload page to demo entity extraction and SOAP generation without audio files.

## Notes

- For best local transcription results, use clear audio with minimal background noise.
- The `base` Whisper model is fast but less accurate than `small` or `medium` models.
- Set `WHISPER_MODEL=small` in `.env` for better accuracy (slower processing).
