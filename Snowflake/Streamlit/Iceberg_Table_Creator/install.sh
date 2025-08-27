#!/bin/bash

# 🧊 Iceberg Table Creator - One-Command Installer
# This script sets up everything you need to run the app

set -e  # Exit on any error

echo "🧊 Welcome to Iceberg Table Creator Setup!"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python is installed
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_status "Found Python $PYTHON_VERSION"

# Check Python version (3.8+)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    print_error "Python 3.8+ is required. Found version $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
print_info "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
print_status "Virtual environment created"

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_status "Pip upgraded"

# Install requirements
print_info "Installing Python packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    print_status "All packages installed successfully"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Check for AWS credentials
print_info "Checking AWS credentials..."
AWS_CREDS_PATH="$HOME/.aws/credentials"
if [ -f "$AWS_CREDS_PATH" ]; then
    print_status "AWS credentials file found"
else
    print_warning "AWS credentials not found at $AWS_CREDS_PATH"
    echo ""
    echo "📝 Create your AWS credentials file:"
    echo "mkdir -p ~/.aws"
    echo "cat > ~/.aws/credentials << EOF"
    echo "[default]"
    echo "aws_access_key_id = YOUR_ACCESS_KEY_ID"
    echo "aws_secret_access_key = YOUR_SECRET_ACCESS_KEY"
    echo "EOF"
    echo ""
fi

# Check for Snowflake connections
print_info "Checking Snowflake connections..."
SF_CONN_PATH="$HOME/.snowflake/connections.toml"
if [ -f "$SF_CONN_PATH" ]; then
    print_status "Snowflake connections file found"
else
    print_warning "Snowflake connections not found at $SF_CONN_PATH"
    echo ""
    echo "📝 Create your Snowflake connections file:"
    echo "mkdir -p ~/.snowflake"
    echo "cat > ~/.snowflake/connections.toml << EOF"
    echo "[DEMO_PRAJAGOPAL_PUBLIC]"
    echo "account = \"YOUR_ACCOUNT\""
    echo "user = \"YOUR_USERNAME\""
    echo "password = \"YOUR_PASSWORD\""
    echo "database = \"YOUR_DATABASE\""
    echo "schema = \"YOUR_SCHEMA\""
    echo "EOF"
    echo ""
fi

# Create run script
print_info "Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
echo "🧊 Starting Iceberg Table Creator..."
source venv/bin/activate
streamlit run Iceberg_Table_Creator.py
EOF
chmod +x run.sh
print_status "Run script created"

echo ""
echo "🎉 Installation Complete!"
echo "======================="
echo ""
print_status "Setup successful! Here's what to do next:"
echo ""
echo "1️⃣  Configure your connections (if not done already):"
echo "   • AWS: ~/.aws/credentials"
echo "   • Snowflake: ~/.snowflake/connections.toml"
echo ""
echo "2️⃣  Run the app:"
echo "   ./run.sh"
echo ""
echo "3️⃣  Open your browser to: http://localhost:8501"
echo ""
print_info "Need help? Check the README.md for detailed setup instructions!"
echo ""
echo "🚀 Happy table creating! ✨"
