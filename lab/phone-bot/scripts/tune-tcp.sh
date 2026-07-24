#!/usr/bin/env bash
# TCP tuning for multi-device ADB (15+ WiFi devices)
# Run with: sudo bash scripts/tune-tcp.sh

set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root: sudo bash scripts/tune-tcp.sh"
  exit 1
fi

echo "Phone Bot — TCP Tuning for Multi-Device ADB"
echo "============================================"
echo ""

# Reduce SYN retries (faster failure detection)
echo "Setting net.ipv4.tcp_syn_retries = 3"
sysctl -w net.ipv4.tcp_syn_retries=3

# Reuse TIME_WAIT sockets
echo "Setting net.ipv4.tcp_tw_reuse = 1"
sysctl -w net.ipv4.tcp_tw_reuse=1

# Increase local port range (more concurrent connections)
echo "Setting net.ipv4.ip_local_port_range = 10000 65000"
sysctl -w net.ipv4.ip_local_port_range="10000 65000"

# Faster keepalive (detect WiFi drops sooner)
echo "Setting TCP keepalive: 30s / 5s / 3 probes"
sysctl -w net.ipv4.tcp_keepalive_time=30
sysctl -w net.ipv4.tcp_keepalive_intvl=5
sysctl -w net.ipv4.tcp_keepalive_probes=3

echo ""
echo "✅ TCP tuning applied. Settings are temporary (reset on reboot)."
echo "   To make permanent, add to /etc/sysctl.conf"
