#!/bin/bash
# DevOps Made Simple - Full Content Automation Setup
# Run this script to install all automated cron jobs
#
# Schedule:
#   - Content Intel Report: Every 2 days at 8:00 AM
#   - Weekly Newsletter Generator: Every Sunday at 6:00 AM
#   - LinkedIn Post Generator: Every Sunday at 9:00 AM (after newsletters)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="/sessions/quirky-brave-hopper/mnt/Newsletter"
LOG_DIR="$WORKSPACE/automation/logs"

mkdir -p "$LOG_DIR"

# Write the cron jobs
crontab -l 2>/dev/null | grep -v "content_intel_report\|newsletter_generator\|linkedin_post_generator" > /tmp/existing_cron

cat >> /tmp/existing_cron << 'CRON'
# === DevOps Made Simple Automation ===
# Content Intel Report - Every 2 days at 8:00 AM
0 8 */2 * * /sessions/quirky-brave-hopper/mnt/Newsletter/automation/run_intel_report.sh >> /sessions/quirky-brave-hopper/mnt/Newsletter/automation/logs/intel_report.log 2>&1
# Weekly Newsletter Generator - Every Sunday at 6:00 AM
0 6 * * 0 /sessions/quirky-brave-hopper/mnt/Newsletter/automation/run_newsletter_generator.sh >> /sessions/quirky-brave-hopper/mnt/Newsletter/automation/logs/newsletter_generator.log 2>&1
# LinkedIn Post Generator - Every Sunday at 9:00 AM
0 9 * * 0 /sessions/quirky-brave-hopper/mnt/Newsletter/automation/run_linkedin_posts.sh >> /sessions/quirky-brave-hopper/mnt/Newsletter/automation/logs/linkedin_posts.log 2>&1
CRON

crontab /tmp/existing_cron
rm /tmp/existing_cron

echo "Automation installed. Cron jobs:"
crontab -l | grep -A1 "DevOps\|Content Intel\|Newsletter\|LinkedIn"
echo ""
echo "Logs will be written to: $LOG_DIR"
