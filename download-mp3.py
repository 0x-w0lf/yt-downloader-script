#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
from yt_dlp import YoutubeDL

def build_opts(outdir, kbps, allow_playlist, cookies_from, cookies_file):
    o = {
        "format": "bestaudio/best",
        "outtmpl": str(Path(outdir) / "%(title).200B [%(id)s].%(ext)s"),
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": kbps}],
        "noplaylist": not allow_playlist,
        "ignoreerrors": True,
        "quiet": False,
    }
    if cookies_from:
        parts = cookies_from.split(":", 1)
        o["cookiesfrombrowser"] = (parts[0],) if len(parts) == 1 else (parts[0], parts[1])
    if cookies_file:
        o["cookiefile"] = cookies_file
    return o

def main():
    p = argparse.ArgumentParser(prog="download-mp3", description="Download YouTube audio as MP3")
    p.add_argument("urls", nargs="*", help="Video or playlist URLs")
    p.add_argument("-f", "--file", help="Text file with one URL per line")
    p.add_argument("-q", "--quality", default="192", choices=["128","160","192","256","320"])
    p.add_argument("--allow-playlist", action="store_true")
    p.add_argument("-o", "--outdir", default=".")
    p.add_argument("--cookies-from", dest="cookies_from", help="Browser or browser:profile (safari|chrome|brave|firefox)")
    p.add_argument("--cookies-file", dest="cookies_file", help="Path to Netscape cookies.txt")
    a = p.parse_args()

    outdir = Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    urls = list(a.urls)
    if a.file:
        urls += [line.strip() for line in Path(a.file).read_text().splitlines() if line.strip()]
    if not urls:
        urls = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]
    if not urls:
        print("No URLs provided", file=sys.stderr); sys.exit(2)

    code = YoutubeDL(build_opts(outdir, a.quality, a.allow_playlist, a.cookies_from, a.cookies_file)).download(urls)
    sys.exit(code if isinstance(code, int) else 0)

if __name__ == "__main__":
    main()

