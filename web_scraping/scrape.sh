#!/bin/bash
# Web Scraping Suite - Easy Runner
# Usage: ./scrape.sh [method] [url]
# Example: ./scrape.sh cypress https://shopee.co.th/

set -e

# Default values
METHOD="${1:-all}"
URL="${2:-https://shopee.co.th/}"
OUTPUT_DIR="output"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Web Scraping Suite${NC}"
echo -e "${BLUE}===================${NC}"
echo -e "📍 URL: ${YELLOW}$URL${NC}"
echo -e "🔧 Method: ${YELLOW}$METHOD${NC}"
echo -e "📁 Output: ${YELLOW}$OUTPUT_DIR${NC}"
echo ""

# Check dependencies
echo -e "${BLUE}🔍 Checking dependencies...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.x${NC}"
    exit 1
fi

# Check Node.js for Cypress
if [[ "$METHOD" == "cypress" || "$METHOD" == "all" ]]; then
    if ! command -v node &> /dev/null; then
        echo -e "${YELLOW}⚠️  Node.js not found. Cypress method will be skipped.${NC}"
    else
        echo -e "${GREEN}✅ Node.js found: $(node --version)${NC}"
    fi
fi

# Check Python packages
if ! python3 -c "import requests, bs4" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Installing required Python packages...${NC}"
    pip3 install requests beautifulsoup4 lxml
fi

# Check Selenium
if [[ "$METHOD" == "selenium" || "$METHOD" == "all" ]]; then
    if ! python3 -c "import selenium" &> /dev/null; then
        echo -e "${YELLOW}⚠️  Selenium not found. Installing...${NC}"
        pip3 install selenium
    fi
fi

# Check Playwright
if [[ "$METHOD" == "playwright" || "$METHOD" == "all" ]]; then
    if ! python3 -c "import playwright" &> /dev/null; then
        echo -e "${YELLOW}⚠️  Playwright not found. Installing...${NC}"
        pip3 install playwright
        playwright install
    fi
fi

echo -e "${GREEN}✅ Dependencies checked${NC}"
echo ""

# Run the scraper
echo -e "${BLUE}🏃 Running scraper...${NC}"
echo ""

python3 scraper.py --method "$METHOD" --url "$URL" --output-dir "$OUTPUT_DIR"

# Show output directory contents
echo ""
echo -e "${BLUE}📋 Output files:${NC}"
ls -la "$OUTPUT_DIR"/ | grep -E "\.(html|json)$" || echo "No files found"

echo ""
echo -e "${GREEN}🎉 Scraping completed!${NC}"

# Offer to open the output directory
if command -v open &> /dev/null; then
    read -p "🔍 Open output directory? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "$OUTPUT_DIR"
    fi
fi