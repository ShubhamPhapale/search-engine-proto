#!/bin/bash

# PySearch Setup Script
# This script sets up the PySearch search engine environment

set -e

echo "🔍 PySearch - Google-like Search Engine Setup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

# Check if Python is installed
check_python() {
    print_section "Checking Python Installation"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_status "Python $PYTHON_VERSION found"
        
        # Check if version is 3.9 or higher
        if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)"; then
            print_status "Python version is compatible (3.9+)"
        else
            print_error "Python 3.9 or higher is required"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        exit 1
    fi
}

# Setup virtual environment
setup_venv() {
    print_section "Setting up Virtual Environment"
    
    if [ -d "search_env" ]; then
        print_warning "Virtual environment already exists"
        read -p "Do you want to recreate it? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf search_env
        else
            return 0
        fi
    fi
    
    print_status "Creating virtual environment..."
    python3 -m venv search_env
    
    print_status "Activating virtual environment..."
    source search_env/bin/activate
    
    print_status "Upgrading pip..."
    pip install --upgrade pip
}

# Install dependencies
install_dependencies() {
    print_section "Installing Dependencies"
    
    if [ ! -f "search_env/bin/activate" ]; then
        print_error "Virtual environment not found"
        exit 1
    fi
    
    source search_env/bin/activate
    
    print_status "Installing Python packages..."
    pip install -r requirements.txt
    
    print_status "Dependencies installed successfully"
}

# Initialize the search engine
initialize_engine() {
    print_section "Initializing Search Engine"
    
    source search_env/bin/activate
    
    if [ -f "database.db" ]; then
        print_warning "Database already exists"
        read -p "Do you want to recreate it with demo data? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -f database.db
            print_status "Running demo setup..."
            python3 main.py
        fi
    else
        print_status "Running demo setup..."
        python3 main.py
    fi
}

# Test the installation
test_installation() {
    print_section "Testing Installation"
    
    source search_env/bin/activate
    
    print_status "Running search engine tests..."
    python3 main.py test
    
    print_status "Testing API demo..."
    python3 demo_api.py
}

# Docker setup
setup_docker() {
    print_section "Docker Setup (Optional)"
    
    if command -v docker &> /dev/null; then
        print_status "Docker found"
        read -p "Do you want to build Docker image? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Building Docker image..."
            docker build -t pysearch:latest .
            print_status "Docker image built successfully"
            
            print_status "Testing Docker container..."
            docker run --rm -d -p 8081:8080 --name test-pysearch pysearch:latest
            sleep 5
            
            if curl -f http://localhost:8081/ > /dev/null 2>&1; then
                print_status "Docker container test successful"
            else
                print_warning "Docker container test failed"
            fi
            
            docker stop test-pysearch > /dev/null 2>&1 || true
        fi
    else
        print_warning "Docker not found - skipping Docker setup"
    fi
}

# Display final instructions
show_instructions() {
    print_section "Setup Complete!"
    
    echo -e "${GREEN}✅ PySearch is ready to use!${NC}\n"
    
    echo "📖 Quick Start Commands:"
    echo "  • Activate environment:    source search_env/bin/activate"
    echo "  • Start web server:        python3 main.py server --port 8080"
    echo "  • Test search:             python3 main.py test"
    echo "  • Crawl new websites:      python3 main.py crawl <URLs>"
    echo "  • Run API demo:            python3 demo_api.py"
    
    echo -e "\n🌐 Web Interface:"
    echo "  • Local:                   http://127.0.0.1:8080"
    echo "  • Network:                 http://$(hostname -I | awk '{print $1}'):8080"
    
    if command -v docker &> /dev/null && docker images | grep -q pysearch; then
        echo -e "\n🐳 Docker Commands:"
        echo "  • Run container:           docker run -p 8080:8080 pysearch:latest"
        echo "  • Run with compose:        docker-compose up"
    fi
    
    echo -e "\n📚 Documentation:"
    echo "  • README.md for detailed usage"
    echo "  • PROJECT_SUMMARY.md for overview"
    
    echo -e "\n🎉 Happy searching!"
}

# Main execution
main() {
    check_python
    setup_venv
    install_dependencies
    initialize_engine
    test_installation
    setup_docker
    show_instructions
}

# Run main function
main "$@"
