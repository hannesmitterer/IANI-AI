# Euystacio Forensic Monitor

## Overview

The **Euystacio Forensic Monitor** is a proactive security countermeasure that monitors system activity for malicious behavior, automatically isolates suspicious IP addresses using iptables, and sends real-time alerts to system administrators via Telegram.

This tool is part of the **Euystacio Framework** - a comprehensive security architecture designed to protect systems from unauthorized access and malicious activity.

## Features

### 🔍 Forensic Monitoring
- **Authentication Log Analysis**: Monitors failed login attempts across the system
- **Network Connection Monitoring**: Detects unusual network patterns like SYN floods
- **Intelligent Threat Detection**: Uses configurable thresholds to identify suspicious activity
- **Automated IP Blocking**: Automatically isolates malicious IPs using iptables

### 📱 Telegram Notifications
- **Real-time Alerts**: Instant notifications when threats are detected and blocked
- **Detailed Information**: Includes blocked IP, reason, and timestamp
- **Easy Configuration**: Simple setup with bot token and chat ID

### 📊 Comprehensive Logging
- **Error Logging**: All errors are logged for debugging and audit purposes
- **Activity Tracking**: Complete record of all blocked IPs with reasons
- **Cron Job Logging**: Separate log for scheduled executions

### ⚙️ Automated Execution
- **Periodic Scanning**: Runs automatically approximately every 7 hours (00:12, 07:12, 14:12, 21:12)
- **Cron Integration**: Easy setup via automated installation script
- **System-wide Availability**: Installed in `/usr/local/bin/` for easy access

> **Note**: The original requirement was every 432 minutes (7.2 hours), but since cron doesn't support intervals that don't divide evenly into 60 minutes, the schedule is configured to run at specific times throughout the day for approximately the same frequency.

## Installation

### Prerequisites

- Linux system with root/sudo access
- `iptables` installed and configured
- `curl` (for Telegram notifications)
- `cron` service running

### Quick Installation

1. Clone or download the repository:
   ```bash
   git clone https://github.com/hannesmitterer/IANI-AI.git
   cd IANI-AI
   ```

2. Make the setup script executable:
   ```bash
   chmod +x setup_forensic_monitor.sh
   ```

3. Run the setup script as root:
   ```bash
   sudo ./setup_forensic_monitor.sh
   ```

4. Follow the interactive prompts to configure Telegram notifications (optional)

The setup script will:
- ✅ Install the forensic monitor to `/usr/local/bin/`
- ✅ Set executable permissions
- ✅ Configure Telegram notifications (if provided)
- ✅ Add a cron job for automated execution every 432 minutes
- ✅ Create necessary log files
- ✅ Run a test execution

## Configuration

### Telegram Notifications

To enable Telegram notifications, you need:

1. **Telegram Bot Token**: Create a bot using [@BotFather](https://t.me/botfather) on Telegram
2. **Chat ID**: Get your chat ID from [@userinfobot](https://t.me/userinfobot)

#### Option 1: Configure During Setup
The setup script will prompt you to enter these values during installation.

#### Option 2: Manual Configuration
Create or edit `/etc/euystacio_forensic_monitor.env`:

```bash
# Euystacio Forensic Monitor - Configuration
TELEGRAM_TOKEN="your_bot_token_here"
TELEGRAM_CHAT_ID="your_chat_id_here"
```

#### Option 3: Environment Variables
Export the variables before running the script:

```bash
export TELEGRAM_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

### Detection Thresholds

You can customize detection thresholds by editing the script variables:

```bash
# Maximum failed login attempts before blocking
MAX_LOGIN_ATTEMPTS=5

# Time window for analysis (in minutes)
SCAN_DURATION_MINUTES=30
```

### Cron Schedule

The default schedule runs approximately every 7 hours at specific times: **00:12, 07:12, 14:12, and 21:12** daily. This approximates the requested 432-minute (7.2 hour) interval.

> **Why not exactly 432 minutes?** Cron only supports intervals that divide evenly into 60 minutes. Since 432 minutes equals 7 hours and 12 minutes, we use specific time-based scheduling instead.

To modify the schedule:

```bash
# Edit the crontab
sudo crontab -e

# Current schedule (runs ~every 7 hours)
12 0,7,14,21 * * * . /etc/euystacio_forensic_monitor.env && /usr/local/bin/euystacio_forensic_monitor.sh >> /var/log/euystacio_forensic_monitor_cron.log 2>&1

# Example: Run every hour instead
0 * * * * . /etc/euystacio_forensic_monitor.env && /usr/local/bin/euystacio_forensic_monitor.sh >> /var/log/euystacio_forensic_monitor_cron.log 2>&1

# Example: Run every 2 hours
0 */2 * * * . /etc/euystacio_forensic_monitor.env && /usr/local/bin/euystacio_forensic_monitor.sh >> /var/log/euystacio_forensic_monitor_cron.log 2>&1
```

## Usage

### Manual Execution

Run the script manually at any time:

```bash
# With Telegram notifications (if configured in env file)
sudo /usr/local/bin/euystacio_forensic_monitor.sh

# With environment variables
sudo TELEGRAM_TOKEN="your_token" TELEGRAM_CHAT_ID="your_chat_id" /usr/local/bin/euystacio_forensic_monitor.sh
```

### View Logs

Monitor the forensic monitor activity:

```bash
# Main log file
sudo tail -f /var/log/euystacio_forensic_monitor.log

# Blocked IPs log
sudo tail -f /var/log/euystacio_blocked_ips.log

# Cron execution log
sudo tail -f /var/log/euystacio_forensic_monitor_cron.log
```

### Check Blocked IPs

View all currently blocked IPs:

```bash
sudo iptables -L INPUT -v -n | grep DROP
```

### Unblock an IP

To remove an IP from the block list:

```bash
sudo iptables -D INPUT -s <IP_ADDRESS> -j DROP
```

## Log Files

| File | Purpose |
|------|---------|
| `/var/log/euystacio_forensic_monitor.log` | Main activity and error log |
| `/var/log/euystacio_blocked_ips.log` | Record of all blocked IPs with timestamps and reasons |
| `/var/log/euystacio_forensic_monitor_cron.log` | Output from cron job executions |

## Security Considerations

1. **Root Privileges**: The script requires root privileges to modify iptables rules
2. **Log File Permissions**: Log files are created with 644 permissions for security
3. **Telegram Credentials**: Stored in `/etc/euystacio_forensic_monitor.env` with 600 permissions
4. **Blocking Persistence**: iptables rules are not persistent across reboots by default
   - To make rules persistent, install `iptables-persistent` package:
     ```bash
     sudo apt-get install iptables-persistent
     ```

## Troubleshooting

### Script Not Running via Cron

1. Check if cron service is running:
   ```bash
   sudo systemctl status cron
   ```

2. Verify cron job is installed:
   ```bash
   sudo crontab -l | grep euystacio
   ```

3. Check cron log for errors:
   ```bash
   sudo tail -f /var/log/euystacio_forensic_monitor_cron.log
   ```

### Telegram Notifications Not Working

1. Verify credentials are correct in `/etc/euystacio_forensic_monitor.env`
2. Check if curl is installed: `which curl`
3. Test the Telegram bot manually:
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage" \
     -d chat_id="<YOUR_CHAT_ID>" \
     -d text="Test message"
   ```

### No IPs Being Blocked

1. Check if there are actually failed login attempts:
   ```bash
   sudo grep -i "failed\|failure" /var/log/auth.log
   ```

2. Verify detection thresholds are appropriate for your environment
3. Ensure iptables is properly configured and accessible

## Uninstallation

To remove the forensic monitor:

```bash
# Remove cron job
sudo crontab -l | grep -v euystacio_forensic_monitor.sh | sudo crontab -

# Remove script
sudo rm /usr/local/bin/euystacio_forensic_monitor.sh

# Remove configuration
sudo rm /etc/euystacio_forensic_monitor.env

# Optionally remove logs
sudo rm /var/log/euystacio_forensic_monitor*.log
sudo rm /var/log/euystacio_blocked_ips.log
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│         Euystacio Forensic Monitor                  │
└─────────────────────────────────────────────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
    ┌───────▼────────┐    ┌────────▼─────────┐
    │ Authentication │    │    Network       │
    │  Log Analysis  │    │ Connection Monitor│
    └───────┬────────┘    └────────┬─────────┘
            │                       │
            └───────────┬───────────┘
                        │
                ┌───────▼────────┐
                │  Threat        │
                │  Detection     │
                └───────┬────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
    ┌───────▼────────┐    ┌────────▼─────────┐
    │   iptables     │    │    Telegram      │
    │   IP Block     │    │  Notification    │
    └────────────────┘    └──────────────────┘
```

## Contributing

This project is part of the **IANI-AI / Euystacio Framework**. Contributions are welcome!

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please visit:
- GitHub Repository: https://github.com/hannesmitterer/IANI-AI

---

🛡️ **Protected by the Euystacio Framework**

*"Materie will frei sein. Sempre in Costante."*
