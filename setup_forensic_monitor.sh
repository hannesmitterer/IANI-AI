#!/bin/bash

################################################################################
# Euystacio Forensic Monitor - Setup Script
# 
# This script automates the deployment of the Euystacio Forensic Monitor:
# - Moves the script to /usr/local/bin/
# - Sets executable permissions
# - Configures Telegram notifications
# - Sets up automated execution via cron (every 432 minutes)
#
# Author: IANI-AI / Euystacio Framework
# Version: 1.0.0
################################################################################

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_NAME="euystacio_forensic_monitor.sh"
INSTALL_DIR="/usr/local/bin"
INSTALL_PATH="$INSTALL_DIR/$SCRIPT_NAME"
CRON_INTERVAL_MINUTES=432

################################################################################
# Utility Functions
################################################################################

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"
}

################################################################################
# Verification Functions
################################################################################

check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This script must be run as root or with sudo privileges"
        print_info "Please run: sudo $0"
        exit 1
    fi
}

check_dependencies() {
    print_info "Checking system dependencies..."
    
    local missing_deps=()
    
    # Check for iptables
    if ! command -v iptables &> /dev/null; then
        missing_deps+=("iptables")
    fi
    
    # Check for curl (needed for Telegram notifications)
    if ! command -v curl &> /dev/null; then
        print_warning "curl is not installed. Telegram notifications will not work."
        print_info "To install curl:"
        print_info "  Debian/Ubuntu: apt-get install curl"
        print_info "  RHEL/CentOS: yum install curl"
    fi
    
    # Check for cron
    if ! command -v crontab &> /dev/null; then
        missing_deps+=("cron")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        print_info "Please install the missing dependencies and run this script again."
        exit 1
    fi
    
    print_success "All required dependencies are installed"
}

check_script_exists() {
    if [ ! -f "$SCRIPT_NAME" ]; then
        print_error "Forensic monitor script '$SCRIPT_NAME' not found in current directory"
        print_info "Please ensure you are running this setup script from the same directory as $SCRIPT_NAME"
        exit 1
    fi
}

################################################################################
# Installation Functions
################################################################################

install_script() {
    print_info "Installing forensic monitor script to $INSTALL_PATH..."
    
    # Create backup if script already exists
    if [ -f "$INSTALL_PATH" ]; then
        local backup_path="${INSTALL_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
        print_warning "Existing script found. Creating backup at $backup_path"
        cp "$INSTALL_PATH" "$backup_path"
    fi
    
    # Copy script to installation directory
    if cp "$SCRIPT_NAME" "$INSTALL_PATH"; then
        print_success "Script copied to $INSTALL_PATH"
    else
        print_error "Failed to copy script to $INSTALL_PATH"
        exit 1
    fi
    
    # Set executable permissions
    if chmod +x "$INSTALL_PATH"; then
        print_success "Executable permissions set on $INSTALL_PATH"
    else
        print_error "Failed to set executable permissions"
        exit 1
    fi
    
    # Verify installation
    if [ -x "$INSTALL_PATH" ]; then
        print_success "Script installed successfully and is executable"
    else
        print_error "Script installation verification failed"
        exit 1
    fi
}

configure_telegram() {
    print_header "Telegram Notification Configuration"
    
    print_info "Telegram notifications allow the system to alert you when IPs are blocked."
    print_info "You will need:"
    print_info "  1. A Telegram Bot Token (from @BotFather)"
    print_info "  2. Your Telegram Chat ID (from @userinfobot)"
    echo
    
    read -p "Do you want to configure Telegram notifications now? (y/n): " -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your Telegram Bot Token: " telegram_token
        read -p "Enter your Telegram Chat ID: " telegram_chat_id
        
        # Create environment file for credentials
        local env_file="/etc/euystacio_forensic_monitor.env"
        
        cat > "$env_file" << EOF
# Euystacio Forensic Monitor - Configuration
# Generated on $(date)

# Telegram Notification Settings
TELEGRAM_TOKEN="$telegram_token"
TELEGRAM_CHAT_ID="$telegram_chat_id"
EOF
        
        chmod 600 "$env_file"
        print_success "Telegram configuration saved to $env_file"
        print_info "The cron job will be configured to use these credentials"
        
        return 0
    else
        print_warning "Skipping Telegram configuration"
        print_info "You can configure it later by setting TELEGRAM_TOKEN and TELEGRAM_CHAT_ID"
        print_info "environment variables or by editing /etc/euystacio_forensic_monitor.env"
        return 1
    fi
}

setup_cron_job() {
    print_header "Cron Job Configuration"
    
    print_info "Setting up automated execution every $CRON_INTERVAL_MINUTES minutes..."
    
    # Check if environment file exists
    local env_file="/etc/euystacio_forensic_monitor.env"
    local env_source=""
    
    if [ -f "$env_file" ]; then
        env_source=". $env_file && "
    fi
    
    # Create cron job entry
    # 432 minutes = 7 hours 12 minutes
    # Since cron doesn't support 432-minute intervals directly, we'll run at specific times
    # to approximate every 7.2 hours: 00:00, 07:12, 14:24, 21:36 (roughly 3 times per day at 7.2 hour intervals)
    local cron_cmd="${env_source}$INSTALL_PATH >> /var/log/euystacio_forensic_monitor_cron.log 2>&1"
    local cron_schedule="12 0,7,14,21 * * *"  # Runs at 00:12, 07:12, 14:12, 21:12 (approximately every 7 hours)
    local cron_entry="$cron_schedule $cron_cmd"
    
    print_info "Note: Cron does not support exact $CRON_INTERVAL_MINUTES minute intervals."
    print_info "The job will run approximately every 7 hours at: 00:12, 07:12, 14:12, 21:12"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "$INSTALL_PATH"; then
        print_warning "Cron job for forensic monitor already exists"
        read -p "Do you want to update it? (y/n): " -r
        echo
        
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Keeping existing cron job"
            return 0
        fi
        
        # Remove old entry
        crontab -l 2>/dev/null | grep -v "$INSTALL_PATH" | crontab -
        print_info "Removed old cron job entry"
    fi
    
    # Add new cron job
    (crontab -l 2>/dev/null; echo "$cron_entry") | crontab -
    
    if [ $? -eq 0 ]; then
        print_success "Cron job added successfully"
        print_info "Schedule: Approximately every 7 hours (00:12, 07:12, 14:12, 21:12)"
        print_info "Command: $cron_cmd"
    else
        print_error "Failed to add cron job"
        print_info "You can manually add the following line to your crontab:"
        print_info "$cron_entry"
        exit 1
    fi
}

create_log_files() {
    print_info "Creating log file directories..."
    
    local log_files=(
        "/var/log/euystacio_forensic_monitor.log"
        "/var/log/euystacio_blocked_ips.log"
        "/var/log/euystacio_forensic_monitor_cron.log"
    )
    
    for log_file in "${log_files[@]}"; do
        touch "$log_file" 2>/dev/null
        chmod 644 "$log_file" 2>/dev/null
    done
    
    print_success "Log files created"
}

################################################################################
# Testing Function
################################################################################

test_installation() {
    print_header "Installation Test"
    
    print_info "Running a test execution of the forensic monitor..."
    echo
    
    # Run the script in test mode
    if [ -f "/etc/euystacio_forensic_monitor.env" ]; then
        . /etc/euystacio_forensic_monitor.env
        export TELEGRAM_TOKEN
        export TELEGRAM_CHAT_ID
    fi
    
    $INSTALL_PATH
    
    if [ $? -eq 0 ]; then
        print_success "Test execution completed successfully"
        print_info "Check /var/log/euystacio_forensic_monitor.log for details"
    else
        print_warning "Test execution completed with warnings/errors"
        print_info "Please check the logs for more information"
    fi
}

################################################################################
# Main Installation Process
################################################################################

main() {
    print_header "Euystacio Forensic Monitor - Setup"
    
    print_info "This script will install and configure the Euystacio Forensic Monitor"
    print_info "Version: 1.0.0"
    echo
    
    # Verification steps
    check_root
    check_dependencies
    check_script_exists
    
    # Installation steps
    install_script
    create_log_files
    
    # Configuration steps
    local telegram_configured=false
    if configure_telegram; then
        telegram_configured=true
    fi
    
    setup_cron_job
    
    # Test installation
    echo
    read -p "Do you want to run a test execution now? (y/n): " -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        test_installation
    fi
    
    # Final summary
    print_header "Installation Complete"
    
    print_success "Euystacio Forensic Monitor has been installed successfully!"
    echo
    print_info "Configuration Summary:"
    print_info "  • Script location: $INSTALL_PATH"
    print_info "  • Execution schedule: Approximately every 7 hours (00:12, 07:12, 14:12, 21:12)"
    print_info "  • Log file: /var/log/euystacio_forensic_monitor.log"
    print_info "  • Blocked IPs log: /var/log/euystacio_blocked_ips.log"
    
    if $telegram_configured; then
        print_info "  • Telegram notifications: Enabled"
    else
        print_info "  • Telegram notifications: Not configured"
    fi
    
    echo
    print_info "Next steps:"
    print_info "  1. Monitor the logs to ensure the script runs correctly"
    print_info "  2. Review blocked IPs in /var/log/euystacio_blocked_ips.log"
    
    if ! $telegram_configured; then
        print_info "  3. Configure Telegram notifications by editing /etc/euystacio_forensic_monitor.env"
    fi
    
    echo
    print_success "🛡️ System protected by Euystacio Framework"
    echo
}

# Execute main function
main
exit $?
