#!/bin/bash
set -e

REPO="AirysDark/SourceForge"
DEFAULT_INSTALL="/opt/sourceforge"

echo "========================================="
echo " SourceForge Installer (Universal)"
echo "========================================="

# Detect architecture
ARCH=$(uname -m)
OS=$(uname -s)

echo "Detected OS: $OS"
echo "Detected Architecture: $ARCH"

if [[ "$ARCH" == "armv7l" ]]; then
  PLATFORM="ARMv7 (Raspberry Pi 3)"
elif [[ "$ARCH" == "aarch64" ]]; then
  PLATFORM="ARM64"
elif [[ "$ARCH" == "x86_64" ]]; then
  PLATFORM="x86_64"
else
  PLATFORM="Unknown"
fi

echo "Platform: $PLATFORM"

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
install_if_missing openssl openssl

# Check Docker
if ! command -v docker >/dev/null 2>&1; then
  if [ "$WSL_MODE" = true ]; then
    echo ""
    echo "Docker not available in WSL."
    echo "Enable WSL integration in Docker Desktop:"
    echo "Docker Desktop → Settings → Resources → WSL Integration"
    exit 1
  else
    echo "Docker not found. Installing..."
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl enable docker || true
    sudo systemctl start docker || true
    sudo usermod -aG docker $USER
    echo ""
    echo "Docker installed."
    echo "Log out and back in, then re-run installer."
    exit 0
  fi
fi

echo "Docker detected."

# Check Docker Compose v2
if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 not detected."
  echo "Please update Docker."
  exit 1
fi

echo "Docker Compose detected."

# Install location
read -p "Install directory [$DEFAULT_INSTALL]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_INSTALL}

sudo mkdir -p "$INSTALL_DIR"
sudo chown $USER:$USER "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "Detecting latest release from GitHub..."

LATEST_JSON=$(curl -s https://api.github.com/repos/$REPO/releases/latest)

DOWNLOAD_URL=$(echo "$LATEST_JSON" | grep -oP '"browser_download_url":\s*"\K[^"]*SourceForge\.zip')

if [ -z "$DOWNLOAD_URL" ]; then
  echo "Could not find SourceForge.zip in latest release."
  exit 1
fi

VERSION=$(echo "$LATEST_JSON" | grep -oP '"tag_name":\s*"\K[^"]*')

echo "Latest version detected: $VERSION"
echo "Downloading..."

curl -L -o SourceForge.zip "$DOWNLOAD_URL"

rm -rf SourceForge
mkdir SourceForge

echo "Extracting..."
unzip -q SourceForge.zip -d SourceForge

cd SourceForge

if [ -f docker-compose.yml ]; then
  echo "Creating .env..."
  JWT_SECRET=$(openssl rand -hex 32)

  cat > .env <<EOF
DATABASE_URL=postgresql://sourceforge:sourceforge@db:5432/sourceforge
SF_JWT_SECRET=$JWT_SECRET
ENV=prod
EOF
fi

echo "Starting containers..."
docker compose up --build -d

# Determine access URL
if [ "$WSL_MODE" = true ]; then
  ACCESS_URL="http://localhost"
else
  ACCESS_URL="http://$(hostname -I | awk '{print $1}')"
fi

echo ""
echo "========================================="
echo " SourceForge $VERSION Installed"
echo " Access it at:"
echo " $ACCESS_URL"
echo "========================================="