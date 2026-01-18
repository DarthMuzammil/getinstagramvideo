from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

def resolve_instagram_mp4(instagram_url: str) -> str:
    """
    Uses yt-dlp to resolve direct MP4 URL
    """
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-f", "mp4",
                "-g",
                instagram_url
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        mp4_url = result.stdout.strip()

        if not mp4_url.startswith("http"):
            raise Exception("Invalid MP4 URL")

        return mp4_url

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/convert")
def convert_instagram_to_mp4(payload: dict):
    """
    Request:
    { "url": "https://www.instagram.com/reel/XXXX/" }
    """
    instagram_url = payload.get("url")

    if not instagram_url:
        raise HTTPException(status_code=422, detail="Instagram URL missing")

    mp4_url = resolve_instagram_mp4(instagram_url)
    return {"mp4_url": mp4_url}