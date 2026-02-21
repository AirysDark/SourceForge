#!/bin/bash
set -e

REPO="AirysDark/SourceForge"
INSTALL_BASE="/opt/sourceforge"
INSTALL_DIR="$INSTALL_BASE/SourceForge"

echo "========================================="
echo " SourceForge Updater (Auto Version)"
echo "========================================="

if [ ! -d "$INSTALL_DIR" ]; then
  echo "SourceForge not found at $INSTALL_DIR"
  exit 1
fi

cd "$INSTALL_BASE"

echo "Checking latest release..."

LATEST_JSON=$(curl -s https://api.github.com/repos/$REPO/releases/latest)

DOWNLOAD_URL=$(echo "$LATEST_JSON" | grep browser_download_url | grep SourceForge.zip | cut -d '"' -f 4)

if [ -z "$DOWNLOAD_URL" ]; then
  echo "Could not find SourceForge.zip in latest release."
  exit 1
fi

VERSION=$(echo "$LATEST_JSON" | grep tag_name | cut -d '"' -f 4)

echo "Latest version: $VERSION"
echo "Downloading update..."

curl -L -o SourceForge.zip "$DOWNLOAD_URL"

echo "Stopping containers..."
cd "$INSTALL_DIR"
docker compose down || docker-compose down

cd "$INSTALL_BASE"

rm -rf SourceForge
mkdir SourceForge

echo "Extracting update..."
unzip -q SourceForge.zip -d SourceForge

cd SourceForge

echo "Rebuilding..."
docker compose up --build -d || docker-compose up --build -d

echo ""
echo "========================================="
echo " Updated to version $VERSION"
echo "========================================="