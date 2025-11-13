#!/bin/bash

# 🎬 SauceDemo Demo Setup Script
# This script sets up Streamlit and ngrok for live demo

set -e

echo "🎬 Setting up SauceDemo Live Demo..."
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python $python_version found"
echo ""

# Install demo dependencies
echo "📦 Installing demo dependencies..."
pip install streamlit pyngrok pandas --break-system-packages --quiet
echo ""

# Check if ngrok auth token is set
echo "🔑 Checking ngrok authentication..."
if [ -z "$NGROK_AUTHTOKEN" ]; then
    echo ""
    echo "⚠️  ngrok authentication token not found!"
    echo ""
    echo "To get your ngrok auth token:"
    echo "1. Sign up at: https://dashboard.ngrok.com/signup"
    echo "2. Copy your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "3. Set it as environment variable:"
    echo "   export NGROK_AUTHTOKEN='your_token_here'"
    echo ""
    echo "Or set it in your .env file:"
    echo "   echo 'NGROK_AUTHTOKEN=your_token_here' >> .env"
    echo ""
    read -p "Do you want to enter your ngrok token now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your ngrok auth token: " ngrok_token
        export NGROK_AUTHTOKEN="$ngrok_token"
        echo "NGROK_AUTHTOKEN=$ngrok_token" >> .env
        echo "✓ Token saved to .env file"
    fi
else
    echo "✓ ngrok token found"
fi
echo ""

# Test imports
echo "🧪 Testing imports..."
python3 -c "import streamlit; import pyngrok; print('✓ All imports successful')"
echo ""

echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Run the demo:  ./run_demo.sh"
echo "2. Or manually:   streamlit run demo_app_basic.py"
echo ""