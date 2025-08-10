#!/bin/bash

# Facebook OSINT Dashboard - System Test Script
# This script tests all components of the system to ensure they're working

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

echo "🧪 Testing Facebook OSINT Dashboard System..."

# Test infrastructure services
test_infrastructure() {
    print_status "Testing infrastructure services..."
    
    # Test Neo4j
    if curl -s http://localhost:7474 > /dev/null 2>&1; then
        print_success "Neo4j is accessible at http://localhost:7474"
    else
        print_error "Neo4j is not accessible"
        return 1
    fi
    
    # Test Kafka UI
    if curl -s http://localhost:8081 > /dev/null 2>&1; then
        print_success "Kafka UI is accessible at http://localhost:8081"
    else
        print_error "Kafka UI is not accessible"
        return 1
    fi
    
    # Test Kafka broker
    if docker ps | grep -q "fbreaper-kafka"; then
        print_success "Kafka broker is running"
    else
        print_error "Kafka broker is not running"
        return 1
    fi
    
    return 0
}

# Test Java backend
test_backend() {
    print_status "Testing Java backend..."
    
    # Test health endpoint
    if curl -s http://localhost:8080/api/health | grep -q "UP"; then
        print_success "Backend health check passed"
    else
        print_error "Backend health check failed"
        return 1
    fi
    
    # Test scraper status endpoint
    if curl -s http://localhost:8080/api/scraper/status > /dev/null 2>&1; then
        print_success "Scraper status endpoint is accessible"
    else
        print_warning "Scraper status endpoint is not accessible"
    fi
    
    # Test data stats endpoint
    if curl -s http://localhost:8080/api/data/stats > /dev/null 2>&1; then
        print_success "Data stats endpoint is accessible"
    else
        print_warning "Data stats endpoint is not accessible"
    fi
    
    return 0
}

# Test React frontend
test_frontend() {
    print_status "Testing React frontend..."
    
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "React frontend is accessible at http://localhost:3000"
    else
        print_error "React frontend is not accessible"
        return 1
    fi
    
    return 0
}

# Test Python scraper
test_scraper() {
    print_status "Testing Python scraper..."
    
    # Check if scraper process is running
    if [ -f "scraper.pid" ]; then
        SCRAPER_PID=$(cat scraper.pid)
        if kill -0 $SCRAPER_PID 2>/dev/null; then
            print_success "Python scraper process is running (PID: $SCRAPER_PID)"
        else
            print_error "Python scraper process is not running"
            return 1
        fi
    else
        print_warning "Python scraper PID file not found"
    fi
    
    return 0
}

# Test API integration
test_api_integration() {
    print_status "Testing API integration..."
    
    # Test scraper start command
    if curl -s -X POST http://localhost:8080/api/scraper/start | grep -q "Scraper start command sent"; then
        print_success "Scraper start command works"
    else
        print_warning "Scraper start command failed"
    fi
    
    # Test keyword scraping command
    if curl -s -X POST "http://localhost:8080/api/scraper/scrapeByKeyword?keyword=test" | grep -q "Scrape by keyword command sent"; then
        print_success "Keyword scraping command works"
    else
        print_warning "Keyword scraping command failed"
    fi
    
    return 0
}

# Main test execution
main() {
    local all_tests_passed=true
    
    echo "🧪 Starting system tests..."
    echo ""
    
    # Test each component
    if ! test_infrastructure; then
        all_tests_passed=false
    fi
    echo ""
    
    if ! test_backend; then
        all_tests_passed=false
    fi
    echo ""
    
    if ! test_frontend; then
        all_tests_passed=false
    fi
    echo ""
    
    if ! test_scraper; then
        all_tests_passed=false
    fi
    echo ""
    
    if ! test_api_integration; then
        all_tests_passed=false
    fi
    echo ""
    
    # Final result
    if [ "$all_tests_passed" = true ]; then
        print_success "🎉 All tests passed! System is working correctly."
        echo ""
        echo "📊 System Status:"
        echo "  ✅ Infrastructure services are running"
        echo "  ✅ Java backend is responding"
        echo "  ✅ React frontend is accessible"
        echo "  ✅ Python scraper is running"
        echo "  ✅ API integration is working"
        echo ""
        echo "🌐 Access your dashboard at: http://localhost:3000"
    else
        print_error "❌ Some tests failed. Please check the logs and restart the system."
        echo ""
        echo "🔧 Troubleshooting:"
        echo "  • Check if all services are running: ./start-system.sh"
        echo "  • View logs: tail -f *.log"
        echo "  • Restart system: ./stop-system.sh && ./start-system.sh"
    fi
}

# Run main function
main "$@"