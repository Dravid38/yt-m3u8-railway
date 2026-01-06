from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Railway yt-dlp m3u8 API running 🚀"

@app.route("/m3u8")
def get_m3u8():
    yt_url = request.args.get("url")

    if not yt_url:
        return jsonify({"error": "YouTube URL missing"}), 400

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
        "extract_flat": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(yt_url, download=False)

    m3u8_links = []

    for f in info.get("formats", []):
        if f.get("protocol") in ["m3u8", "m3u8_native"]:
            m3u8_links.append({
                "format_id": f.get("format_id"),
                "resolution": f.get("resolution"),
                "url": f.get("url")
            })

    return jsonify({
        "title": info.get("title"),
        "m3u8_count": len(m3u8_links),
        "m3u8_links": m3u8_links
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
