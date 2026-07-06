#!/usr/bin/env bash
set -euo pipefail

PROJECT="$HOME/sd/personalProjects/yt-downloader-script"
TARGET="$HOME/bin/download-mp3"

mkdir -p "$HOME/bin"

cat > "$TARGET" <<SH
#!/usr/bin/env bash
set -euo pipefail
exec "$PROJECT/.venv/bin/python" "$PROJECT/download-mp3.py" "\$@"
SH

chmod +x "$TARGET"

echo "Installed wrapper at $TARGET"
echo "Make sure ~/bin is in your PATH."
