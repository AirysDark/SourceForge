#!/bin/bash
set -e

REPO="AirysDark/SourceForge"
DEFAULT_INSTALL="/opt/sourceforge"

echo "========================================="
echo " SourceForge Installer (Auto Version)"
echo "========================================="

# Detect architecture
ARCH=$(uname -m)
echo "Detected architecture: $ARCH"

# Ensure required tools exist
install_if_missing() {
  if ! command -v $1 >/dev/null 2>&1; then
    echo "$1 not found. Installing..."
    sudo apt update
    sudo apt install -y $2
  fi
}

install_if_missing curl curl
install_if_missing unzip unzip
install_if_missing openssl openssl

# Check Docker
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Installing..."
  sudo apt update
  sudo apt install docker.io docker-compose -y
  sudo systemctl enable docker || true
  sudo systemctl start docker || true
  sudo usermod -aG docker $USER
  echo "Docker installed. Please log out and back in, then re-run."
  exit 0
fi

echo "Docker detected."

# Install location
read -p "Install directory [$DEFAULT_INSTALL]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_INSTALL}

sudo mkdir -p "$INSTALL_DIR"
sudo chown $USER:$USER "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "Detecting latest release from GitHub..."

LATEST_JSON=$(curl -s https://api.github.com/repos/$REPO/releases/latest)

DOWNLOAD_URL=$(echo "$LATEST_JSON" | grep browser_download_url | grep SourceForge.zip | cut -d '"' -f 4)

if [ -z "$DOWNLOAD_URL" ]; then
  echo "Could not find SourceForge.zip in latest release."
  exit 1
fi

VERSION=$(echo "$LATEST_JSON" | grep tag_name | cut -d '"' -f 4)

echo "Latest version detected: $VERSION"
echo "Downloading from: $DOWNLOAD_URL"

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
docker compose up --build -d || docker-compose up --build -d

IP=$(hostname -I | awk '{print $1}')

echo ""
echo "========================================="
echo " SourceForge $VERSION Installed"
echo " Open in browser:"
echo " http://$IP"
echo "========================================="
