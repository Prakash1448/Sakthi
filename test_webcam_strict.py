"""
Test webcam proctoring with STRICT settings to prevent false warnings.
This test verifies that normal face detection does NOT increment warnings.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from proctoring_service import create_proctoring_session, process_monitoring_event
import time

print("="*60)
print("WEBCAM STRICT TEST - No False Warnings")
print("="*60)

# Test: 30 frames with normal face should produce ZERO warnings
print("\n[Test] Sending 30 frames with proper face detected...")
print("Expected: 0 warnings (no false increments)\n")

session_id = create_proctoring_session()
print(f"Session created: {session_id[:8]}...")

warning_count = 0

for i in range(30):
    result = process_monitoring_event(session_id, {
        "face_detected": True,
        "face_count": 1,
        "violation_type": None,  # No violation
        "confidence": 0.95,
        "timestamp": time.time(),
        "event_id": f"normal_frame_{i}"
    })
    
    if result['warning_count'] > warning_count:
        print(f"\n❌ FAILED at frame {i+1}")
        print(f"   Unexpected warning issued!")
        print(f"   Warning count jumped from {warning_count} to {result['warning_count']}")
        print(f"   Status: {result['monitoring_status']}")
        sys.exit(1)
    
    warning_count = result['warning_count']
    
    # Show progress every 10 frames
    if (i+1) % 10 == 0:
        print(f"  Frame {i+1}/30: Warnings={warning_count}, Status={result['monitoring_status']}")
    
    time.sleep(0.05)  # Small delay

print(f"\n{'='*60}")
if warning_count == 0:
    print("✅ TEST PASSED!")
    print(f"   30 frames processed")
    print(f"   0 warnings issued")
    print(f"   Final status: {result['monitoring_status']}")
    print("\n   Webcam is working correctly - no false warnings!")
else:
    print("❌ TEST FAILED!")
    print(f"   {warning_count} warnings issued incorrectly")

print("="*60)
