import io
import math
import wave
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException

from app.ml.mla import mla


ARTIFACTS_ROOT = Path(__file__).resolve().parents[1] / "artifacts"


def _compute_rms(chunk: bytes, sample_width: int) -> float:
    if not chunk or sample_width <= 0:
        return 0.0

    usable = len(chunk) - (len(chunk) % sample_width)
    if usable <= 0:
        return 0.0

    total = 0.0
    count = 0
    offset = 0

    while offset < usable:
        sample = int.from_bytes(
            chunk[offset : offset + sample_width],
            byteorder="little",
            signed=True,
        )
        total += float(sample * sample)
        count += 1
        offset += sample_width

    if count == 0:
        return 0.0

    return math.sqrt(total / count)


def _write_dummy_spectrogram_svg(
    file_path: Path,
    kind: str,
    start_sec: float,
    end_sec: float,
    score: float,
) -> None:
    bar_width = 16
    gap = 6
    left = 24
    bars = 14
    max_bar = 70
    top = 20
    color = "#2b7be6" if kind == "mel" else "#2ba36f"

    bar_markup: list[str] = []
    for index in range(bars):
        # Deterministic pseudo-pattern so visuals are stable per segment.
        level = ((index * 17) + int(start_sec * 19) + int(end_sec * 13) + int(score * 100)) % max_bar
        h = max(10, level)
        x = left + index * (bar_width + gap)
        y = top + (max_bar - h)
        bar_markup.append(
            f'<rect x="{x}" y="{y}" width="{bar_width}" height="{h}" rx="3" fill="{color}" opacity="0.85" />'
        )

    svg = (
        "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"320\" height=\"110\" viewBox=\"0 0 320 110\">"
        "<rect width=\"320\" height=\"110\" fill=\"#0f172a\" />"
        f"<text x=\"14\" y=\"16\" fill=\"#e2e8f0\" font-size=\"11\" font-family=\"Arial\">{kind.upper()} spectrogram</text>"
        f"<text x=\"14\" y=\"103\" fill=\"#94a3b8\" font-size=\"10\" font-family=\"Arial\">{start_sec:.2f}s - {end_sec:.2f}s | score {score:.2f}</text>"
        + "".join(bar_markup)
        + "</svg>"
    )
    file_path.write_text(svg, encoding="utf-8")


def _extract_suspicious_windows(wav_bytes: bytes, max_parts: int = 3) -> list[tuple[float, float, float]]:
    try:
        with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
            sample_width = wav_file.getsampwidth()
            sample_rate = wav_file.getframerate()
            total_frames = wav_file.getnframes()

            if sample_rate <= 0 or total_frames <= 0:
                return []

            window_frames = max(1, int(sample_rate * 0.75))
            windows: list[tuple[int, float, float, float]] = []
            frame_cursor = 0

            while frame_cursor < total_frames:
                read_frames = min(window_frames, total_frames - frame_cursor)
                chunk = wav_file.readframes(read_frames)
                if not chunk:
                    break

                rms = _compute_rms(chunk, sample_width)
                start_sec = frame_cursor / sample_rate
                end_sec = min((frame_cursor + read_frames) / sample_rate, total_frames / sample_rate)
                windows.append((frame_cursor, start_sec, end_sec, rms))
                frame_cursor += read_frames

            if not windows:
                return []

            max_rms = max(window[3] for window in windows) or 1.0
            top_windows = sorted(windows, key=lambda item: item[3], reverse=True)[:max_parts]
            top_windows.sort(key=lambda item: item[1])

            return [
                (start_sec, end_sec, round(min(1.0, rms / max_rms), 2))
                for _, start_sec, end_sec, rms in top_windows
            ]
    except wave.Error:
        return []


def _build_suspicious_parts(wav_bytes: bytes, analysis_id: str) -> list[dict]:
    windows = _extract_suspicious_windows(wav_bytes)
    if not windows:
        return []

    analysis_dir = ARTIFACTS_ROOT / analysis_id
    analysis_dir.mkdir(parents=True, exist_ok=True)

    parts: list[dict] = []
    for index, (start_sec, end_sec, score) in enumerate(windows):
        mel_name = f"part-{index}-mel.svg"
        mfcc_name = f"part-{index}-mfcc.svg"
        mel_path = analysis_dir / mel_name
        mfcc_path = analysis_dir / mfcc_name

        _write_dummy_spectrogram_svg(mel_path, "mel", start_sec, end_sec, score)
        _write_dummy_spectrogram_svg(mfcc_path, "mfcc", start_sec, end_sec, score)

        parts.append(
            {
                "start_sec": round(start_sec, 3),
                "end_sec": round(end_sec, 3),
                "score": score,
                "mel_image_url": f"/artifacts/{analysis_id}/{mel_name}",
                "mfcc_image_url": f"/artifacts/{analysis_id}/{mfcc_name}",
            }
        )

    return parts


def run_inference(wav_bytes: bytes) -> dict:
    if not wav_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        result = mla.predict(wav_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Model inference failed.") from exc

    if "status" not in result or "accuracy" not in result:
        raise HTTPException(
            status_code=500,
            detail="Model output must include 'status' and 'accuracy'.",
        )

    status = str(result["status"]).lower().strip()
    accuracy = float(result["accuracy"])

    if status not in {"ai", "real"}:
        raise HTTPException(status_code=500, detail="Model status must be 'ai' or 'real'.")

    if accuracy < 0.0 or accuracy > 1.0:
        raise HTTPException(status_code=500, detail="Model accuracy must be in [0, 1].")

    analysis_id = uuid4().hex[:12]
    suspicious_parts = _build_suspicious_parts(wav_bytes, analysis_id) if status == "ai" else []

    return {
        "status": status,
        "accuracy": accuracy,
        "analysis_id": analysis_id,
        "suspicious_parts": suspicious_parts,
    }
