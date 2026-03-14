# AI Voice Detector Backend

FastAPI API for voice classification (`.wav` in, JSON out).

## Run (PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Docs: `http://127.0.0.1:8000/docs`

## Endpoints

- `GET /health` -> `{"status": "ok"}`
- `POST /predict` -> multipart form-data field `file` (`.wav` only)

## Real Model Setup

`app/ml/mla.py` now uses your real Wav2Vec2 model artifacts at runtime.

Provide model artifacts using one of these options:

1. `MODEL_DIR`: local folder containing files like `config.json`, `tokenizer_config.json`, `vocab.json`, and `model.safetensors`.
2. `MODEL_ZIP_PATH`: local zip (for example your `final_model.zip`) that contains the trained model folder.
3. `MODEL_RELEASE_URL`: direct URL to your Git release zip asset. Backend downloads and caches it automatically.

By default, backend is preconfigured to download:

`https://github.com/Nikola0505stag/FMI-Code-2026/releases/download/v1.0/final_model.zip`

Downloaded and extracted artifacts are cached under `backend/model/`.

Optional env vars:

- `MODEL_TARGET_SR` (default `16000`)
- `MODEL_TARGET_DURATION_SEC` (default `3.0`)
- `MODEL_DEVICE` (`cpu` or `cuda`, default `cpu`)

## Test `/predict`

```powershell
curl.exe -X POST "http://127.0.0.1:8000/predict" `
  -H "accept: application/json" `
  -F "file=@C:\path\to\sample.wav;type=audio/wav"
```

## Response Format

```json
{
  "status": "ai",
  "accuracy": 0.91,
  "analysis_id": "a1b2c3d4e5f6",
  "suspicious_parts": [
    {
      "start_sec": 2.25,
      "end_sec": 3.0,
      "score": 0.88,
      "mel_image_url": "/artifacts/a1b2c3d4e5f6/part-0-mel.png",
      "mfcc_image_url": "/artifacts/a1b2c3d4e5f6/part-0-mfcc.png"
    }
  ]
}
```

Notes:

- `suspicious_parts` is empty when `status` is `real`.
- The `/artifacts/...` URLs are static files served by FastAPI.
- Artifact images are real feature visualizations generated from audio windows (not placeholders).

## Model Contract

`app/ml/mla.py` -> `MLA.predict(wav_bytes: bytes) -> dict`

```python
{"status": "ai" | "real", "accuracy": 0.0..1.0}
```

`app/services/inference.py` enriches this model output with:

- `analysis_id`
- `suspicious_parts[]`
  - `start_sec`, `end_sec`, `score`
  - `mel_image_url`, `mfcc_image_url`

Static files are exposed at `/artifacts/<analysis_id>/...`.

## Common Errors

- `400`: invalid file or not real WAV
- `413`: file too large
- `500`: model inference failure
