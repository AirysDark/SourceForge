#!/bin/bash

set -e

echo "=== SourceForge Alpha Installer ==="

# Detect architecture
ARCH=$(uname -m)
echo "Detected architecture: $ARCH"

if [[ "$ARCH" == "armv7l" ]]; then
    PLATFORM="ARMv7 (Raspberry Pi 3)"
elif [[ "$ARCH" == "aarch64" ]]; then
    PLATFORM="ARM64"
elif [[ "$ARCH" == "x86_64" ]]; then
    PLATFORM="x86_64"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

echo "Platform: $PLATFORM"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing..."
    sudo apt update
    sudo apt install docker.io docker-compose -y
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker $USER
    echo "Docker installed. Please log out and back in, then re-run installer."
    exit 0
fi

echo "Docker detected."

# Ask install location
read -p "Install directory [/opt/sourceforge]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-/opt/sourceforge}

sudo mkdir -p $INSTALL_DIR
sudo chown $USER:$USER $INSTALL_DIR
cd $INSTALL_DIR

# Ask admin details
read -p "Admin username: " ADMIN_USER
read -s -p "Admin password: " ADMIN_PASS
echo ""

# Generate JWT secret
JWT_SECRET=$(openssl rand -hex 32)
echo "Generated secure JWT secret."

# Download Alpha stack
echo "Downloading SourceForge Alpha stack..."
curl -L -o sourceforge-alpha.zip https://your-download-link/sourceforge-alpha-full-stack.zip

unzip -o sourceforge-alpha.zip
cd sourceforge-alpha-full-stack

# Create .env
cat > .env <<EOF
DATABASE_URL=postgresql://sourceforge:sourceforge@db:5432/sourceforge
SF_JWT_SECRET=$JWT_SECRET
ENV=prod
EOF

echo "Environment configured."

# Start containers
echo "Starting containers..."
docker compose up --build -d || docker-compose up --build -d

sleep 5

# Verify health
if curl -s http://localhost/api/health | grep -q "ok"; then
    echo "Backend healthy."
else
    echo "Backend failed to start."
    exit 1
fi

IP=$(hostname -I | awk '{print $1}')

echo ""
echo "===================================="
echo "SourceForge Alpha Installed!"
echo "Access it at:"
echo "http://$IP"
echo "===================================="