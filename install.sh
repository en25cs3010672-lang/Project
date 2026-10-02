#!/bin/bash

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Electricity Consumption Analyzer - Setup${NC}"
echo -e "${BLUE}================================================${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
if python3 -m venv venv; then
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${BLUE}Installing dependencies from requirements.txt...${NC}"
if pip install -r requirements.txt; then
    echo -e "${GREEN}✅ All dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✅ Setup complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${BLUE}To run the application:${NC}"
echo -e "${YELLOW}1. Activate the virtual environment:${NC}"
echo -e "${YELLOW}   source venv/bin/activate${NC}"
echo ""
echo -e "${YELLOW}2. Run the Streamlit app:${NC}"
echo -e "${YELLOW}   streamlit run electricity_analyzer.py${NC}"
echo ""
echo -e "${BLUE}To deactivate the virtual environment:${NC}"
echo -e "${YELLOW}   deactivate${NC}"
