# download-mp3 — YouTube → MP3 (no metadata, no artwork)

Small Python CLI that downloads **audio only** from YouTube as **MP3**, without embedding metadata or cover art. Saves to the **current directory** by default, supports playlists, browser cookies, and a `--clean` flag to free space before downloading.

> Use it only for content you own or have permission to download. Respect YouTube’s Terms of Service and local laws.

---

## Table of Contents
- [English](#english)
  - [Requirements (macOS)](#requirements-macos)
  - [Quick Install](#quick-install)
  - [Optional: Global Wrapper](#optional-global-wrapper)
  - [Usage](#usage)
  - [Options](#options)
  - [Cookies & Auth](#cookies--auth)
  - [macOS Permissions Tips](#macos-permissions-tips)
  - [Output Naming](#output-naming)
  - [Troubleshooting](#troubleshooting)
- [Español](#español)
  - [Requisitos (macOS)](#requisitos-macos)
  - [Instalación Rápida](#instalación-rápida)
  - [Opcional: Wrapper Global](#opcional-wrapper-global)
  - [Uso](#uso)
  - [Opciones](#opciones)
  - [Cookies y Autenticación](#cookies-y-autenticación)
  - [Permisos en macOS](#permisos-en-macos)
  - [Nombres de Salida](#nombres-de-salida)
  - [Solución de Problemas](#solución-de-problemas)
- [Script Reference](#script-reference)

---

## English

### Requirements (macOS)
- Homebrew
- Python 3.11+ (works great with 3.13)
- FFmpeg (via Homebrew)
- `yt-dlp` (installed in a virtualenv)

### Quick Install
```bash
# Project layout (example)
mkdir -p ~/sd/personalProjects/yt-downloader-script
cd ~/sd/personalProjects/yt-downloader-script

# Python virtual environment
python3 -m venv yt-downloader-script
source yt-downloader-script/bin/activate

# Dependencies inside venv
python -m pip install -U pip -r requirements.txt
brew install ffmpeg

# Put the script at repo root (same level as the venv folder)
# File: download-mp3.py
chmod +x download-mp3.py
```

### Optional: Global Wrapper
Run without activating the venv (adjust paths only if your folder differs):
```bash
mkdir -p ~/bin
cat > ~/bin/download-mp3 <<'SH'
#!/usr/bin/env bash
set -euo pipefail
VENV="$HOME/sd/personalProjects/yt-downloader-script/yt-downloader-script"
SCRIPT="$(dirname "$VENV")/download-mp3.py"
if [ ! -f "$SCRIPT" ]; then
  echo "download-mp3: script not found at: $SCRIPT" >&2
  exit 127
fi
exec "$VENV/bin/python" "$SCRIPT" "$@"
SH
chmod +x ~/bin/download-mp3
grep -q 'export PATH="$HOME/bin:$PATH"' ~/.zshrc || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Usage
```bash
# Help
download-mp3 -h

# From file (one URL per line), save into current folder
download-mp3 -f ./urls.txt

# Single URL, 320 kbps
download-mp3 -q 320 "https://www.youtube.com/watch?v=VIDEO_ID"

# Read from stdin
cat urls.txt | download-mp3

# Clean existing MP3s in the output folder before downloading
download-mp3 --clean -f ./urls.txt

# Use browser cookies (Chrome default profile)
download-mp3 --cookies-from chrome:Default -f ./urls.txt
```

### Options
```
download-mp3 [URLs ...]
  -f, --file FILE                    Text file with one URL per line
  -q, --quality {128,160,192,256,320}   MP3 bitrate (default: 192)
      --allow-playlist               Allow full playlist download
  -o, --outdir PATH                  Output directory (default: .)
      --cookies-from BROWSER[:PROFILE]  safari | chrome[:Default] | brave[:Default] | firefox[:profile]
      --cookies-file PATH            Path to a Netscape cookies.txt
      --clean                        Delete *.mp3 in outdir before downloading
  -h, --help
```

### Cookies & Auth
If YouTube asks to sign in or throws “not a bot”, pass cookies:

- **Chrome default profile**
  ```bash
  download-mp3 --cookies-from chrome:Default -f ./urls.txt
  ```
- **Brave**
  ```bash
  download-mp3 --cookies-from brave:Default -f ./urls.txt
  ```
- **Safari** (Terminal needs Full Disk Access)
  ```bash
  download-mp3 --cookies-from safari -f ./urls.txt
  ```
- **cookies.txt** (exported file)
  ```bash
  download-mp3 --cookies-file ./cookies.txt -f ./urls.txt
  ```
Treat `cookies.txt` as a secret (`chmod 600 cookies.txt`) and delete it when done.

### macOS Permissions Tips
- Safari cookies live in protected folders. Go to **System Settings → Privacy & Security → Full Disk Access** and enable your Terminal (and if needed Homebrew’s `Python.app` shown in error paths).
- Chrome/Brave/Firefox may prompt Keychain access the first time—allow it.

### Output Naming
```
<title> [<video_id>].mp3
```

### Troubleshooting
- `command not found: download-mp3` → Add the wrapper to `~/bin` and ensure `~/bin` is on `PATH`, or activate your venv first.
- Still hitting 3.9.x Python? Ensure `which python3` points to your venv when active.
- Safari cookies PermissionError → give Full Disk Access to Terminal (and possibly Brew’s `Python.app`), then restart Terminal.
- Rate limited → add `--cookies-from ...` or try later.

---

## Español

### Requisitos (macOS)
- Homebrew  
- Python 3.11+ (ideal 3.13)  
- FFmpeg (vía Homebrew)  
- `yt-dlp` (instalado en un entorno virtual)

### Instalación Rápida
```bash
# Estructura del proyecto (ejemplo)
mkdir -p ~/sd/personalProjects/yt-downloader-script
cd ~/sd/personalProjects/yt-downloader-script

# Entorno virtual
python3 -m venv yt-downloader-script
source yt-downloader-script/bin/activate

# Dependencias dentro del venv
python -m pip install -U pip -r requirements.txt
brew install ffmpeg

# Coloca el script en la raíz del repo (mismo nivel que la carpeta del venv)
# Archivo: download-mp3.py
chmod +x download-mp3.py
```

### Opcional: Wrapper Global
Para usarlo sin activar el venv (ajusta rutas solo si tu carpeta difiere):
```bash
mkdir -p ~/bin
cat > ~/bin/download-mp3 <<'SH'
#!/usr/bin/env bash
set -euo pipefail
VENV="$HOME/sd/personalProjects/yt-downloader-script/yt-downloader-script"
SCRIPT="$(dirname "$VENV")/download-mp3.py"
if [ ! -f "$SCRIPT" ]; then
  echo "download-mp3: script not found at: $SCRIPT" >&2
  exit 127
fi
exec "$VENV/bin/python" "$SCRIPT" "$@"
SH
chmod +x ~/bin/download-mp3
grep -q 'export PATH="$HOME/bin:$PATH"' ~/.zshrc || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Uso
```bash
# Ayuda
download-mp3 -h

# Desde archivo (una URL por línea), guarda en la carpeta actual
download-mp3 -f ./urls.txt

# Una URL a 320 kbps
download-mp3 -q 320 "https://www.youtube.com/watch?v=VIDEO_ID"

# Leer desde stdin
cat urls.txt | download-mp3

# Limpiar MP3 existentes en la carpeta de salida antes de descargar
download-mp3 --clean -f ./urls.txt

# Usar cookies del navegador (perfil por defecto de Chrome)
download-mp3 --cookies-from chrome:Default -f ./urls.txt
```

### Opciones
```
download-mp3 [URLs ...]
  -f, --file FILE                    Archivo de texto con una URL por línea
  -q, --quality {128,160,192,256,320}   Bitrate MP3 (por defecto: 192)
      --allow-playlist               Permite descargar playlists completas
  -o, --outdir RUTA                  Carpeta de salida (por defecto: .)
      --cookies-from NAVEGADOR[:PERFIL]  safari | chrome[:Default] | brave[:Default] | firefox[:perfil]
      --cookies-file RUTA            Ruta a un cookies.txt (formato Netscape)
      --clean                        Borra los *.mp3 del outdir antes de descargar
  -h, --help
```

### Cookies y Autenticación
Si YouTube pide login o “not a bot”, agrega cookies:

- **Chrome (perfil por defecto)**
  ```bash
  download-mp3 --cookies-from chrome:Default -f ./urls.txt
  ```
- **Brave**
  ```bash
  download-mp3 --cookies-from brave:Default -f ./urls.txt
  ```
- **Safari** (Terminal necesita Full Disk Access)
  ```bash
  download-mp3 --cookies-from safari -f ./urls.txt
  ```
- **cookies.txt** (archivo exportado)
  ```bash
  download-mp3 --cookies-file ./cookies.txt -f ./urls.txt
  ```
Trata `cookies.txt` como un secreto (`chmod 600 cookies.txt`) y bórralo al terminar.

### Permisos en macOS
- Safari guarda cookies en carpetas protegidas. Ve a **System Settings → Privacy & Security → Full Disk Access** y habilita tu Terminal (y si hace falta el `Python.app` de Homebrew).
- Chrome/Brave/Firefox pueden pedir acceso al Llavero la primera vez—acéptalo.

### Nombres de Salida
```
<título> [<video_id>].mp3
```

### Solución de Problemas
- `command not found: download-mp3` → agrega el wrapper a `~/bin` y asegúrate de que `~/bin` está en `PATH`, o activa primero tu venv.
- Sigue saliendo Python 3.9.x → verifica que `which python3` apunte a tu venv cuando esté activo.
- PermissionError con Safari → da Full Disk Access a Terminal (y posiblemente al `Python.app` de Brew) y reinicia la Terminal.
- Limitado por velocidad → añade `--cookies-from ...` o intenta más tarde.

---

## Script Reference

> Code in English, no comments. Includes `--clean` and cookies support.
