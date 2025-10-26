#!/bin/bash

# =============================================================================
# Production Docker Test Runner with Allure Reports
# =============================================================================

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IMAGE_NAME="behave-tests"
REPORTS_DIR="${SCRIPT_DIR}/reports"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
WORKERS=4
OPEN_REPORT=true
CLEAN=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --workers)
            WORKERS="$2"
            shift 2
            ;;
        --no-serve|--no-open)
            OPEN_REPORT=false
            shift
            ;;
        --no-clean)
            CLEAN=false
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --workers N      Number of parallel workers (default: 4)"
            echo "  --no-open        Don't automatically open report (default: opens automatically)"
            echo "  --no-clean       Don't clean previous reports"
            echo "  --help           Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Run '$0 --help' for usage"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}                    🐳 Docker Test Runner with Allure                        ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Clean previous reports
if [ "$CLEAN" = true ]; then
    echo -e "${YELLOW}🧹 Cleaning previous reports...${NC}"
    rm -rf "${REPORTS_DIR}"
    echo -e "${GREEN}   ✓ Cleaned${NC}"
    echo ""
fi

# Create directories
echo -e "${BLUE}📁 Creating report directories...${NC}"
mkdir -p "${REPORTS_DIR}"/{allure-results,allure-results-merged,allure-report,screenshots}
echo -e "${GREEN}   ✓ Created${NC}"
echo ""

# Build Docker image
echo -e "${BLUE}🔨 Building Docker image...${NC}"
docker build -t ${IMAGE_NAME} . > /tmp/docker-build.log 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✓ Build successful${NC}"
else
    echo -e "${RED}   ✗ Build failed! Check /tmp/docker-build.log${NC}"
    cat /tmp/docker-build.log
    exit 1
fi
echo ""

# Run tests
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🧪 Running tests with ${WORKERS} parallel workers...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

docker run --rm \
  -v "${REPORTS_DIR}/allure-results:/app/allure-results" \
  -v "${REPORTS_DIR}/allure-results-merged:/app/allure-results-merged" \
  -v "${REPORTS_DIR}/screenshots:/app/screenshots" \
  ${IMAGE_NAME} \
  python test_runner.py --report --workers ${WORKERS}

TEST_EXIT_CODE=$?
echo ""

if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}❌ Tests failed with exit code ${TEST_EXIT_CODE}${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
fi

# Merge results from subdirectories (PID folders created by parallel workers)
echo -e "${BLUE}🔄 Merging test results from parallel workers...${NC}"
if [ -d "${REPORTS_DIR}/allure-results" ]; then
    # Copy all JSON files from subdirectories to merged directory
    JSON_COUNT=$(find "${REPORTS_DIR}/allure-results" -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$JSON_COUNT" -gt 0 ]; then
        find "${REPORTS_DIR}/allure-results" -name "*.json" -exec cp {} "${REPORTS_DIR}/allure-results-merged/" \; 2>/dev/null
        find "${REPORTS_DIR}/allure-results" -name "*.txt" -exec cp {} "${REPORTS_DIR}/allure-results-merged/" \; 2>/dev/null
        find "${REPORTS_DIR}/allure-results" -name "*.xml" -exec cp {} "${REPORTS_DIR}/allure-results-merged/" \; 2>/dev/null
        echo -e "${GREEN}   ✓ Merged ${JSON_COUNT} result files${NC}"
    else
        echo -e "${YELLOW}   ⚠ No result files found in subdirectories${NC}"
    fi
else
    echo -e "${YELLOW}   ⚠ allure-results directory not found${NC}"
fi
echo ""

# Verify results exist
echo -e "${BLUE}🔍 Verifying test results...${NC}"

RESULT_FILES=$(find "${REPORTS_DIR}/allure-results-merged" -name "*.json" 2>/dev/null | wc -l | tr -d ' ')

if [ "$RESULT_FILES" -eq 0 ]; then
    echo -e "${RED}   ✗ No Allure result files found!${NC}"
    echo -e "${YELLOW}   ℹ️  Expected files in: ${REPORTS_DIR}/allure-results-merged${NC}"
    echo ""
    echo -e "${YELLOW}   Checking what's in the directory:${NC}"
    ls -la "${REPORTS_DIR}/allure-results-merged/" 2>/dev/null || echo "   Directory doesn't exist"
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}❌ Cannot generate report - no test results found${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
else
    echo -e "${GREEN}   ✓ Found ${RESULT_FILES} result files${NC}"
fi
echo ""

# Generate Allure report
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📊 Generating Allure report...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if ! command -v allure &> /dev/null; then
    echo -e "${RED}   ✗ Allure CLI not found!${NC}"
    echo ""
    echo -e "${YELLOW}   Install Allure:${NC}"
    echo -e "${YELLOW}      macOS:   brew install allure${NC}"
    echo -e "${YELLOW}      Linux:   See https://docs.qameta.io/allure/#_installing_a_commandline${NC}"
    echo -e "${YELLOW}      Windows: scoop install allure${NC}"
    echo ""
    echo -e "${BLUE}   Results saved to: ${REPORTS_DIR}/allure-results-merged${NC}"
    echo -e "${BLUE}   You can generate the report manually later with:${NC}"
    echo -e "${BLUE}      allure generate ${REPORTS_DIR}/allure-results-merged -o ${REPORTS_DIR}/allure-report${NC}"
    exit 0
fi

allure generate "${REPORTS_DIR}/allure-results-merged" --clean -o "${REPORTS_DIR}/allure-report"

if [ $? -eq 0 ] || [ -f "${REPORTS_DIR}/allure-report/index.html" ]; then
    echo -e "${GREEN}   ✓ Report generated successfully!${NC}"
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ All done!${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if [ "$OPEN_REPORT" = true ]; then
        echo -e "${BLUE}🌐 Opening report...${NC}"
        echo ""
        
        # Use the standalone open_report.sh script
        if [ -f "${SCRIPT_DIR}/open_report.sh" ]; then
            bash "${SCRIPT_DIR}/open_report.sh"
        else
            echo -e "${YELLOW}⚠️  open_report.sh not found, opening manually...${NC}"
            
            if command -v allure &> /dev/null; then
                allure open "${REPORTS_DIR}/allure-report"
            else
                echo -e "${YELLOW}   Using Python HTTP server${NC}"
                cd "${REPORTS_DIR}/allure-report"
                python3 -m http.server 8080 > /dev/null 2>&1 &
                SERVER_PID=$!
                sleep 2
                open http://localhost:8080
                echo -e "${GREEN}   ✓ Report at http://localhost:8080${NC}"
                wait $SERVER_PID
            fi
        fi
    else
        echo -e "${BLUE}📁 Report location:${NC}"
        echo -e "   ${REPORTS_DIR}/allure-report/index.html"
        echo ""
        echo -e "${BLUE}🚀 To open the report manually:${NC}"
        if command -v allure &> /dev/null; then
            echo -e "   ${YELLOW}allure open ${REPORTS_DIR}/allure-report${NC}"
        else
            echo -e "   ${YELLOW}cd ${REPORTS_DIR}/allure-report && python3 -m http.server 8080${NC}"
            echo -e "   ${YELLOW}Then open: http://localhost:8080${NC}"
        fi
        echo -e "${BLUE}   Or run: ${YELLOW}./open_report.sh${NC}"
        echo ""
    fi
        fi
        echo -e "${BLUE}   Or run: ${YELLOW}./open_report.sh${NC}"
        echo ""
    fi
    
    
    exit $TEST_EXIT_CODE
else
    echo -e "${RED}   ✗ Failed to generate report${NC}"
    exit 1
fi