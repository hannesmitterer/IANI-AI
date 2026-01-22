#!/bin/bash

################################################################################
# Euystacio Forensic Monitor
# 
# A proactive forensic countermeasure script that monitors suspicious activity,
# isolates malicious IPs using iptables, and notifies administrators via Telegram.
#
# Author: IANI-AI / Euystacio Framework
# Version: 1.0.0
# License: See LICENSE file
################################################################################

# Configuration Variables
# Set these variables or export them as environment variables before running
TELEGRAM_TOKEN="${TELEGRAM_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

# Log file location
LOG_FILE="/var/log/euystacio_forensic_monitor.log"
BLOCKED_IPS_FILE="/var/log/euystacio_blocked_ips.log"

# Thresholds for detection
MAX_LOGIN_ATTEMPTS=5
SCAN_DURATION_MINUTES=30

################################################################################
# Logging Functions
################################################################################

log_message() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE" 2>/dev/null || echo "[$timestamp] [$level] $message"
}

log_info() {
    log_message "INFO" "$@"
}

log_error() {
    log_message "ERROR" "$@"
}

log_warning() {
    log_message "WARNING" "$@"
}

################################################################################
# System Verification
################################################################################

verify_dependencies() {
    log_info "Verifying system dependencies..."
    
    # Check if running as root or with sudo privileges
    if [ "$EUID" -ne 0 ]; then
        log_warning "Script is not running as root. Some operations may require sudo."
    fi
    
    # Check if iptables is installed
    if ! command -v iptables &> /dev/null; then
        log_error "iptables is not installed. Please install iptables first."
        log_error "On Debian/Ubuntu: sudo apt-get install iptables"
        log_error "On RHEL/CentOS: sudo yum install iptables"
        return 1
    fi
    
    log_info "iptables is installed and accessible"
    
    # Check if we can write to log file
    if ! touch "$LOG_FILE" 2>/dev/null; then
        log_warning "Cannot write to $LOG_FILE. Logging to console only."
    fi
    
    # Verify curl for Telegram notifications
    if [ -n "$TELEGRAM_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        if ! command -v curl &> /dev/null; then
            log_warning "curl is not installed. Telegram notifications will not work."
        fi
    fi
    
    return 0
}

################################################################################
# Telegram Notification
################################################################################

send_telegram_notification() {
    local message="$1"
    
    # Skip if Telegram credentials are not configured
    if [ -z "$TELEGRAM_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
        log_info "Telegram notifications not configured (TELEGRAM_TOKEN or TELEGRAM_CHAT_ID missing)"
        return 0
    fi
    
    # Check if curl is available
    if ! command -v curl &> /dev/null; then
        log_error "curl is required for Telegram notifications but is not installed"
        return 1
    fi
    
    local api_url="https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage"
    
    # Send notification
    local response=$(curl -s -X POST "$api_url" \
        -d chat_id="$TELEGRAM_CHAT_ID" \
        -d text="$message" \
        -d parse_mode="HTML" 2>&1)
    
    if [ $? -eq 0 ]; then
        log_info "Telegram notification sent successfully"
        return 0
    else
        log_error "Failed to send Telegram notification: $response"
        return 1
    fi
}

################################################################################
# IP Blocking Functions
################################################################################

is_ip_blocked() {
    local ip="$1"
    
    # Check if IP is already in iptables DROP chain
    if sudo iptables -L INPUT -v -n 2>/dev/null | grep -q "$ip"; then
        return 0
    fi
    
    return 1
}

block_ip() {
    local ip="$1"
    local reason="$2"
    
    # Validate IP format (basic validation)
    if ! echo "$ip" | grep -qE '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'; then
        log_error "Invalid IP address format: $ip"
        return 1
    fi
    
    # Check if already blocked
    if is_ip_blocked "$ip"; then
        log_info "IP $ip is already blocked"
        return 0
    fi
    
    # Block the IP using iptables
    if sudo iptables -A INPUT -s "$ip" -j DROP 2>/dev/null; then
        local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        log_info "Successfully blocked IP: $ip (Reason: $reason)"
        echo "[$timestamp] $ip - $reason" >> "$BLOCKED_IPS_FILE"
        
        # Send Telegram notification
        local notification_message="🚨 <b>Euystacio Forensic Alert</b> 🚨\n\n"
        notification_message+="<b>Blocked IP:</b> <code>$ip</code>\n"
        notification_message+="<b>Reason:</b> $reason\n"
        notification_message+="<b>Timestamp:</b> $timestamp\n\n"
        notification_message+="🛡️ System protected by Euystacio Framework"
        
        send_telegram_notification "$notification_message"
        
        return 0
    else
        log_error "Failed to block IP: $ip"
        return 1
    fi
}

################################################################################
# Forensic Analysis Functions
################################################################################

analyze_auth_logs() {
    log_info "Analyzing authentication logs for suspicious activity..."
    
    local suspicious_ips=()
    
    # Check common auth log locations
    local auth_log=""
    if [ -f "/var/log/auth.log" ]; then
        auth_log="/var/log/auth.log"
    elif [ -f "/var/log/secure" ]; then
        auth_log="/var/log/secure"
    else
        log_warning "No authentication log file found"
        return 0
    fi
    
    # Find IPs with failed login attempts in the last SCAN_DURATION_MINUTES
    local cutoff_time=$(date -d "$SCAN_DURATION_MINUTES minutes ago" '+%b %d %H:%M' 2>/dev/null || date -v-${SCAN_DURATION_MINUTES}M '+%b %d %H:%M' 2>/dev/null)
    
    if [ -n "$cutoff_time" ]; then
        # Extract IPs with failed authentication attempts
        local failed_attempts=$(grep -i "failed\|failure\|invalid" "$auth_log" 2>/dev/null | \
            grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' | \
            sort | uniq -c | sort -rn)
        
        while read -r count ip; do
            # Skip empty lines
            if [ -z "$count" ] || [ -z "$ip" ]; then
                continue
            fi
            
            if [ "$count" -ge "$MAX_LOGIN_ATTEMPTS" ]; then
                log_warning "Detected $count failed login attempts from IP: $ip"
                suspicious_ips+=("$ip")
            fi
        done <<< "$failed_attempts"
    fi
    
    # Block suspicious IPs
    for ip in "${suspicious_ips[@]}"; do
        block_ip "$ip" "Excessive failed login attempts ($count attempts detected)"
    done
    
    if [ ${#suspicious_ips[@]} -eq 0 ]; then
        log_info "No suspicious authentication activity detected"
    fi
}

analyze_network_connections() {
    log_info "Analyzing network connections for suspicious patterns..."
    
    # Check for unusual port scanning activity
    # This is a basic implementation - can be enhanced with more sophisticated detection
    
    if command -v netstat &> /dev/null; then
        # Look for IPs with many connections in SYN_RECV state (possible SYN flood)
        local syn_flood_ips=$(netstat -tan 2>/dev/null | grep SYN_RECV | \
            awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | \
            awk -v threshold=20 '$1 >= threshold {print $2}')
        
        if [ -n "$syn_flood_ips" ]; then
            while read -r ip; do
                if [ -n "$ip" ]; then
                    log_warning "Detected possible SYN flood from IP: $ip"
                    block_ip "$ip" "Possible SYN flood attack detected"
                fi
            done <<< "$syn_flood_ips"
        fi
    fi
}

################################################################################
# Main Execution
################################################################################

main() {
    log_info "=== Euystacio Forensic Monitor Started ==="
    log_info "Version: 1.0.0"
    
    # Verify dependencies
    if ! verify_dependencies; then
        log_error "Dependency verification failed. Exiting."
        exit 1
    fi
    
    # Perform forensic analysis
    analyze_auth_logs
    analyze_network_connections
    
    log_info "=== Forensic Monitor Scan Completed ==="
    
    return 0
}

# Execute main function
main
exit $?
