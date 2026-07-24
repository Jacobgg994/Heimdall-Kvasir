#!/usr/bin/env bash
# Quick health check for all connected devices

echo "Phone Bot — Device Health Check"
echo "================================"
echo ""

adb devices | grep -v "List of devices" | grep "device" | cut -f1 | while read serial; do
  echo "📱 $serial"
  echo "   Model:      $(adb -s "$serial" shell getprop ro.product.model 2>/dev/null || echo 'N/A')"
  echo "   Android:    $(adb -s "$serial" shell getprop ro.build.version.release 2>/dev/null || echo 'N/A')"
  echo "   Battery:    $(adb -s "$serial" shell dumpsys battery 2>/dev/null | grep 'level:' | awk '{print $2}')%"
  echo "   Temp:       $(adb -s "$serial" shell dumpsys battery 2>/dev/null | grep 'temperature:' | awk '{print $2}') (raw)"
  echo "   Charging:   $(adb -s "$serial" shell dumpsys battery 2>/dev/null | grep 'AC powered:' | awk '{print $3}')"
  echo "   Resolution: $(adb -s "$serial" shell wm size 2>/dev/null | cut -d' ' -f3)"
  echo ""
done
