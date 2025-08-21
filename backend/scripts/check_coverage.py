#!/usr/bin/env python3
import sys


if len(sys.argv) != 3:
    print("Usage: check_coverage.py <PREVIOUS> <CURRENT>")
    sys.exit(0)

previous_coverage = float(sys.argv[1])
current_coverage = float(sys.argv[2])

print(f"Gefundene Coverage: {current_coverage:.3f}%")
print(f"Erforderlich:      {previous_coverage:.3f}%")

if current_coverage < previous_coverage:
    print(f"❌ Coverage zu niedrig: {current_coverage:.3f}% < {previous_coverage:.3f}%")
    sys.exit(1)
else:
    print(f"✅ Coverage OK: {current_coverage:.3f}% ≥ {previous_coverage:.3f}%")
    sys.exit(0)
