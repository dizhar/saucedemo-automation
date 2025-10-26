#!/bin/bash

# =============================================================================
# Open Allure Report
# Works with or without Allure CLI installed
# =============================================================================

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPORT_DIR="${SCRIPT_DIR}/reports/allure-report"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}           📊 Opening Allure Report                          ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if report exists
if [ ! -d "$REPORT_DIR" ]; then
    echo -e "${RED}❌ Report not found at: ${REPORT_DIR}${NC}"
    echo ""
    echo -e "${YELLOW}Run this first to generate the report:${NC}"
    echo -e "   ${YELLOW}./run_docker_tests.sh${NC}"
    echo ""
    exit 1
fi

if [ ! -f "$REPORT_DIR/index.html" ]; then
    echo -e "${RED}❌ Report appears incomplete (no index.html)${NC}"
    echo ""
    echo -e "${YELLOW}Try regenerating the report:${NC}"
    echo -e "   ${YELLOW}./run_docker_tests.sh${NC}"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Report found${NC}"
echo ""

# Try to open with Allure CLI first
if command -v allure &> /dev/null; then
    echo -e "${BLUE}🚀 Opening report with Allure CLI...${NC}"
    allure open "$REPORT_DIR"
else
    # Fallback to Python HTTP server
    echo -e "${YELLOW}ℹ️  Allure CLI not found, using Python HTTP server${NC}"
    echo ""
    
    # Check if Python 3 is available
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found!${NC}"
        echo ""
        echo -e "${YELLOW}Please install one of:${NC}"
        echo -e "   - Allure CLI: ${YELLOW}brew install allure${NC}"
        echo -e "   - Python 3: ${YELLOW}brew install python3${NC}"
        echo ""
        exit 1
    fi
    
    echo -e "${BLUE}🌐 Starting local web server...${NC}"
    cd "$REPORT_DIR"
    
    # Check if port 8080 is already in use
    if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port 8080 is already in use${NC}"
        echo ""
        echo -e "${BLUE}📊 Report may already be open at: ${GREEN}http://localhost:8080${NC}"
        echo ""
        echo -e "${YELLOW}Opening browser anyway...${NC}"
        open http://localhost:8080
        echo ""
        echo -e "${BLUE}If report doesn't load, try a different port:${NC}"
        echo -e "   ${YELLOW}cd $REPORT_DIR && python3 -m http.server 8081${NC}"
    else
        # Start the server
        python3 -m http.server 8080 > /dev/null 2>&1 &
        SERVER_PID=$!
        
        # Wait for server to start
        sleep 2
        
        # Open browser
        open http://localhost:8080
        
        echo -e "${GREEN}✓ Report opened in browser${NC}"
        echo ""
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}📊 Report available at: ${BLUE}http://localhost:8080${NC}"
        echo -e "${YELLOW}🔧 Server PID: ${SERVER_PID}${NC}"
        echo ""
        echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        
        # Keep the script alive so server keeps running
        wait $SERVER_PID
    fi
fi
