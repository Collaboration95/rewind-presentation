#!/bin/zsh
# Throwaway simulator: create, boot, record ~6 s with simctl io recordVideo, then shut down and delete (only the device this script created).
set -u
OUT=/tmp/rewind-video/in
UDID=$(xcrun simctl create rewind-video-tmp com.apple.CoreSimulator.SimDeviceType.iPhone-17-Pro com.apple.CoreSimulator.SimRuntime.iOS-26-5) || exit 1
echo "created $UDID"
trap 'xcrun simctl shutdown $UDID >/dev/null 2>&1; xcrun simctl delete $UDID >/dev/null 2>&1; echo cleaned' EXIT
start=$(date +%s)
xcrun simctl boot $UDID && xcrun simctl bootstatus $UDID -b
echo "boot took $(( $(date +%s) - start )) s"
xcrun simctl launch $UDID com.apple.mobilesafari >/dev/null 2>&1
sleep 2
xcrun simctl io $UDID recordVideo --codec=h264 --force $OUT/sim-iphone17pro.mov &
RP=$!
sleep 6
kill -INT $RP; wait $RP
ls -la $OUT/sim-iphone17pro.mov
xcrun simctl io $UDID screenshot $OUT/sim-shot.png 2>&1 | tail -1
