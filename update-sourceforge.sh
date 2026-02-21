#!/bin/bash
set -e

REPO="AirysDark/SourceForge"
INSTALL_BASE="/opt/sourceforge"
INSTALL_DIR="$INSTALL_BASE/SourceForge"
BACKUP_DIR="$INSTALL_BASE/backup_$(date +%Y%m%d_%H%M%S)"

echo "========================================="
echo " SourceForge Updater (Universal)"
echo "========================================="

# Detect architecture
ARCH=$(uname -m)
echo "Detected Architecture: $ARCH"

# Detect WSL
if grep -qi microsoft /proc/version 2>/dev/null; then
  echo "Environment: WSL"
  WSL_MODE=true
else
  echo "Environment: Native Linux"
  WSL_MODE=false
fi

# Ensure required tools exist
install_if_missing() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "$1 not found. Installing..."
    sudo apt update
    sudo apt install -y "$2"
  fi
}

install_if_missing curl curl
install_if_missing unzip unzip

# Verify install exists
if [ ! -d "$INSTALL_DIR" ]; then
  echo "SourceForge not found at $INSTALL_DIR"
  exit 1
fi

cd "$INSTALL_BASE"

echo "Checking latest release from GitHub..."

LATEST_JSON=$(curl -s https://api.github.com/repos/$REPO/releases/latest)

DOWNLOAD_URL=$(echo "$LATEST_JSON" | grep -oP '"browser_download_url":\s*"\K[^"]*SourceForge\.zip')

if [ -z "$DOWNLOAD_URL" ]; then
  echo "Could not find SourceForge.zip in latest release."
  exit 1
fi

LATEST_VERSION=$(echo "$LATEST_JSON" | grep -oP '"tag_name":\s*"\K[^"]*')

# Detect current version (if stored)
if [ -f "$INSTALL_DIR/.version" ]; then
  CURRENT_VERSION=$(cat "$INSTALL_DIR/.version")
else
  CURRENT_VERSION="unknown"
fi

echo "Current version: $CURRENT_VERSION"
echo "Latest version:  $LATEST_VERSION"

if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
  echo "Already up to date."
  exit 0
fi

echo "Downloading latest version..."
curl -L -o SourceForge.zip "$DOWNLOAD_URL"

echo "Stopping containers..."
cd "$INSTALL_DIR"
docker compose down

cd "$INSTALL_BASE"

echo "Creating backup at $BACKUP_DIR"
mv SourceForge "$BACKUP_DIR"

mkdir SourceForge

echo "Extracting update..."
unzip -q SourceForge.zip -d SourceForge

cd SourceForge

# Store version marker
echo "$LATEST_VERSION" > .version

echo "Rebuilding containers..."
docker compose up --build -d

echo ""
echo "========================================="
echo " Updated successfully to $LATEST_VERSION"
echo " Backup stored at:"
echo " $BACKUP_DIR"
echo "========================================="