# download-mp3

Small Python CLI to download audio from YouTube as MP3 using `yt-dlp` and FFmpeg.

The script saves files to the current directory by default, supports individual videos, playlists, browser cookies, custom output folders, and optional cleanup of existing MP3 files.

> Use this tool only for content you own, created, licensed, or have permission to download. Respect YouTube’s Terms of Service and local laws.

---

## Features

* Download YouTube audio as MP3.
* Select MP3 bitrate: `128`, `160`, `192`, `256`, or `320`.
* Save output to the current folder or a custom directory.
* Read URLs from command arguments, a text file, or standard input.
* Optional browser cookies support for age-restricted, logged-in, or bot-check scenarios.
* Optional cleanup of existing `.mp3` files before downloading.
* Playlist downloads disabled by default to avoid accidental full-channel or full-playlist downloads.

---

## Project Structure

```text
yt-downloader-script/
├── .gitignore
├── README.md
├── requirements.txt
├── download-mp3.py
├── scripts/
│   └── install-wrapper.sh
└── .venv/                  # local only, ignored by Git
```

The `.venv/` folder is only for your local machine and should never be committed to GitHub.

---

## Requirements

Tested on macOS.

Required:

* Python 3.11+
* Homebrew
* FFmpeg
* Deno
* `yt-dlp`
* `yt-dlp-ejs`

Install system dependencies:

```bash
brew install ffmpeg deno
```

`deno` is used as a JavaScript runtime for newer YouTube extraction paths supported by `yt-dlp-ejs`.

---

## Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd yt-downloader-script
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
python -m pip install -U pip
python -m pip install -U --pre -r requirements.txt
```

Verify the installation:

```bash
python - <<'PY'
import yt_dlp, shutil, sys

print("python:", sys.executable)
print("yt-dlp:", yt_dlp.version.__version__)
print("deno:", shutil.which("deno"))
print("ffmpeg:", shutil.which("ffmpeg"))
PY
```

---

## Optional Global Command

To run the script as `download-mp3` from anywhere, install the wrapper:

```bash
./scripts/install-wrapper.sh
```

Then verify:

```bash
which download-mp3
download-mp3 -h
```

The wrapper expects this project to live at:

```text
~/sd/personalProjects/yt-downloader-script
```

If your path is different, edit `scripts/install-wrapper.sh` before running it.

---

## Usage

### Show Help

```bash
download-mp3 -h
```

Or without the wrapper:

```bash
.venv/bin/python download-mp3.py -h
```

---

### Download One Video

```bash
download-mp3 'https://www.youtube.com/watch?v=VIDEO_ID'
```

With 320 kbps:

```bash
download-mp3 -q 320 'https://www.youtube.com/watch?v=VIDEO_ID'
```

Important: do not escape `?`, `=`, or `&` inside quoted URLs.

Correct:

```bash
download-mp3 'https://www.youtube.com/watch?v=VIDEO_ID'
```

Incorrect:

```bash
download-mp3 'https://www.youtube.com/watch\?v\=VIDEO_ID'
```

---

### Download From a File

Create a text file with one URL per line:

```text
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
https://www.youtube.com/watch?v=VIDEO_ID_3
```

Then run:

```bash
download-mp3 -f urls.txt
```

---

### Read URLs From Standard Input

```bash
cat urls.txt | download-mp3
```

---

### Save to a Custom Output Folder

```bash
download-mp3 -o ~/Downloads/music 'https://www.youtube.com/watch?v=VIDEO_ID'
```

---

### Clean Existing MP3 Files Before Downloading

This deletes existing `.mp3` files in the output folder before starting the download.

```bash
download-mp3 --clean -f urls.txt
```

With a custom folder:

```bash
download-mp3 --clean -o ~/Downloads/music -f urls.txt
```

---

### Allow Playlist Downloads

Playlist downloads are disabled by default.

To allow downloading a full playlist:

```bash
download-mp3 --allow-playlist 'https://www.youtube.com/playlist?list=PLAYLIST_ID'
```

Use this carefully. Some YouTube URLs can redirect to playlists, tabs, or channel upload lists.

---

## Cookies and Authentication

Sometimes YouTube may require login, age verification, or bot-check validation. In those cases, use browser cookies.

### Chrome

```bash
download-mp3 --cookies-from chrome:Default 'https://www.youtube.com/watch?v=VIDEO_ID'
```

### Brave

```bash
download-mp3 --cookies-from brave:Default 'https://www.youtube.com/watch?v=VIDEO_ID'
```

### Safari

```bash
download-mp3 --cookies-from safari 'https://www.youtube.com/watch?v=VIDEO_ID'
```

Safari cookies may require Full Disk Access for your terminal.

On macOS:

```text
System Settings → Privacy & Security → Full Disk Access
```

Enable your terminal app, then restart the terminal.

### cookies.txt

You can also use a Netscape-format cookies file:

```bash
download-mp3 --cookies-file ./cookies.txt 'https://www.youtube.com/watch?v=VIDEO_ID'
```

Treat cookies as secrets:

```bash
chmod 600 cookies.txt
```

Do not commit cookies to Git.

---

## Command Options

```text
download-mp3 [URLs ...]

Options:
  -f, --file FILE
      Text file with one URL per line.

  -q, --quality {128,160,192,256,320}
      MP3 bitrate. Default: 192.

  --allow-playlist
      Allow full playlist downloads.

  -o, --outdir PATH
      Output directory. Default: current directory.

  --cookies-from BROWSER[:PROFILE]
      Load cookies from a browser.
      Examples: chrome:Default, brave:Default, safari.

  --cookies-file PATH
      Path to a Netscape-format cookies.txt file.

  --clean
      Delete existing .mp3 files in the output directory before downloading.

  -h, --help
      Show help.
```

---

## Output Naming

Files are saved as:

```text
<title> [<video_id>].mp3
```

Example:

```text
My Song [abc123XYZ].mp3
```

---

## Updating Dependencies

YouTube changes frequently. If downloads start failing with errors such as `nsig extraction failed`, `SABR streaming`, or `Requested format is not available`, update `yt-dlp` inside the virtual environment:

```bash
cd ~/sd/personalProjects/yt-downloader-script
source .venv/bin/activate

python -m pip install -U pip
python -m pip install -U --pre "yt-dlp[default]" yt-dlp-ejs
python -m pip freeze > requirements.txt
```

Then retry:

```bash
download-mp3 -q 320 'https://www.youtube.com/watch?v=VIDEO_ID'
```

---

## Troubleshooting

### `command not found: download-mp3`

Make sure `~/bin` is in your `PATH`.

For zsh:

```bash
grep -q 'export PATH="$HOME/bin:$PATH"' ~/.zshrc || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Then reinstall the wrapper:

```bash
./scripts/install-wrapper.sh
```

---

### Wrapper Points to an Old Virtual Environment

If you see an error like:

```text
No such file or directory: .../yt-downloader-script/yt-downloader-script/bin/python
```

your wrapper is stale.

Reinstall it:

```bash
cd ~/sd/personalProjects/yt-downloader-script
./scripts/install-wrapper.sh
hash -r
```

---

### `ffmpeg` Not Found

Install FFmpeg:

```bash
brew install ffmpeg
```

Verify:

```bash
which ffmpeg
ffmpeg -version
```

---

### `deno` Not Found

Install Deno:

```bash
brew install deno
```

Verify:

```bash
which deno
deno --version
```

---

### YouTube Bot Check, Login, or Age Restriction

Use browser cookies:

```bash
download-mp3 --cookies-from chrome:Default 'https://www.youtube.com/watch?v=VIDEO_ID'
```

Or:

```bash
download-mp3 --cookies-from brave:Default 'https://www.youtube.com/watch?v=VIDEO_ID'
```

---

### `Requested format is not available`

Update `yt-dlp` and `yt-dlp-ejs`:

```bash
source .venv/bin/activate
python -m pip install -U --pre "yt-dlp[default]" yt-dlp-ejs
```

Then retry with cookies if needed.

---

## Development Notes

Run the script directly during development:

```bash
source .venv/bin/activate
python download-mp3.py -h
```

Check Git status before committing:

```bash
git status --short
```

Expected tracked project files:

```text
.gitignore
README.md
requirements.txt
download-mp3.py
scripts/install-wrapper.sh
```

Expected ignored local files:

```text
.venv/
*.mp3
cookies.txt
.DS_Store
```

---

## Disclaimer

This project is not affiliated with YouTube, Google, FFmpeg, or yt-dlp. It is a small personal CLI wrapper around `yt-dlp` for permitted audio downloads.

