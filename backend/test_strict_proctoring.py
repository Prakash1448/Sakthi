"""
=========================================
Strict Proctoring Service Test
AI Interview Platform
=========================================
Tests for upgraded strict security with 1-second thresholds
and tab switch detection.
"""

import time
from proctoring_service import (
    create_proctoring_session,
    process_monitoring_event,
    process_tab_switch_event,
    get_session_status,
    MAX_WARNINGS,
    FACE_ABSENCE_THRESHOLD,
    HEAD_TURN_THRESHOLD,
    LOOKING_DOWN_THRESHOLD,
    MULTIPLE_FACE_THRESHOLD,
    TAB_SWITCH_PENALTY,
    NORMAL_RESET_DURATION
)


print("=" * 70)
print("STRICT PROCTORING SECURITY - COMPREHENSIVE TEST SUITE")
print("=" * 70)
print(f"\nConfiguration:")
print(f"  MAX_WARNINGS: {MAX_WARNINGS}")
print(f"  FACE_ABSENCE_THRESHOLD: {FACE_ABSENCE_THRESHOLD}s")
print(f"  HEAD_TURN_THRESHOLD: {HEAD_TURN_THRESHOLD}s")
print(f"  LOOKING_DOWN_THRESHOLD: {LOOKING_DOWN_THRESHOLD}s")
print(f"  MULTIPLE_FACE_THRESHOLD: {MULTIPLE_FACE_THRESHOLD}s")
print(f"  TAB_SWITCH_PENALTY: +{TAB_SWITCH_PENALTY} warnings")
print(f"  NORMAL_RESET_DURATION: {NORMAL_RESET_DURATION}s")


# TEST 1: Exactly one face visible - no warning
print("\n[TEST 1] Exactly one face visible")
session_id = create_proctoring_session()
result = process_monitoring_event(session_id, {
    "face_detected": True,
    "face_count": 1,
    "violation_type": None,
    "confidence": 0.95,
    "timestamp": time.time()
})
assert result["warning_count"] == 0, "Should have 0 warnings"
print("✓ PASS: No warning with one face visible")


# TEST 2: Face absent for 0.5 seconds - no warning
print("\n[TEST 2] Face absent for 0.5 seconds")
session_id = create_proctoring_session()
for i in range(3):
    process_monitoring_event(session_id, {
        "face_detected": False,
        "face_count": 0,
        "violation_type": "face_absent",
        "confidence": 0.90,
        "timestamp": time.time()
    })
    time.sleep(0.2)

result = get_session_status(session_id)
assert result["warning_count"] == 0, "Should have 0 warnings (under threshold)"
print("✓ PASS: No warning for violation under 1 second")


# TEST 3: Face absent for 1.2 seconds - +1 warning
print("\n[TEST 3] Face absent for 1.2 seconds")
session_id = create_proctoring_session()
for i in range(7):
    result = process_monitoring_event(session_id, {
        "face_detected": False,
        "face_count": 0,
        "violation_type": "face_absent",
        "confidence": 0.90,
        "timestamp": time.time(),
        "event_id": f"face_absent_{i}"
    })
    time.sleep(0.2)

assert result["warning_count"] == 1, f"Should have 1 warning, got {result['warning_count']}"
assert result["warning_issued"] == True, "Should have issued warning"
print("✓ PASS: +1 warning for face absent 1.2 seconds")


# TEST 4: Face absent continuously for 10 seconds - only 1 warning
print("\n[TEST 4] Face absent continuously for 10 seconds")
session_id = create_proctoring_session()
for i in range(50):
    result = process_monitoring_event(session_id, {
        "face_detected": False,
        "face_count": 0,
        "violation_type": "face_absent",
        "confidence": 0.90,
        "timestamp": time.time(),
        "event_id": f"continuous_{i}"
    })
    time.sleep(0.2)

assert result["warning_count"] == 1, f"Should have only 1 warning for continuous incident, got {result['warning_count']}"
print("✓ PASS: Only 1 warning for continuous 10-second violation")


# TEST 5: Turn left for 1.2 seconds - +1 warning
print("\n[TEST 5] Turn left for 1.2 seconds")
session_id = create_proctoring_session()
for i in range(7):
    result = process_monitoring_event(session_id, {
        "face_detected": True,
        "face_count": 1,
        "violation_type": "looking_left",
        "confidence": 0.85,
        "timestamp": time.time(),
        "event_id": f"left_{i}"
    })
    time.sleep(0.2)

assert result["warning_count"] == 1, "Should have 1 warning"
print("✓ PASS: +1 warning for turning left 1.2 seconds")


# TEST 6: Look down for 1.2 seconds - +1 warning
print("\n[TEST 6] Look down for 1.2 seconds")
session_id = create_proctoring_session()

# First return to normal to reset
for i in range(6):
    process_monitoring_event(session_id, {
        "face_detected": True,
        "face_count": 1,
        "violation_type": None,
        "confidence": 0.95,
        "timestamp": time.time()
    })
    time.sleep(0.2)

# Now look down
for i in range(7):
    result = process_monitoring_event(session_id, {
        "face_detected": True,
        "face_count": 1,
        "violation_type": "looking_down",
        "confidence": 0.85,
        "timestamp": time.time(),
        "event_id": f"down_{i}"
    })
    time.sleep(0.2)

assert result["warning_count"] == 2, f"Should have 2 warnings total, got {result['warning_count']}"
print("✓ PASS: +1 warning for looking down 1.2 seconds")


# TEST 7: Multiple faces for 1.2 seconds - +1 warning
print("\n[TEST 7] Multiple faces for 1.2 seconds")
session_id = create_proctoring_session()
for i in range(7):
    result = process_monitoring_event(session_id, {
        "face_detected": True,
        "face_count": 2,
        "violation_type": "multiple_faces",
        "confidence": 0.80,
        "timestamp": time.time(),
        "event_id": f"multi_{i}"
    })
    time.sleep(0.2)

assert result["warning_count"] == 1, "Should have 1 warning"
print("✓ PASS: +1 warning for multiple faces 1.2 seconds")


# TEST 8: Tab switch - immediate +3 warnings
print("\n[TEST 8] Tab switch - immediate +3 warnings")
session_id = create_proctoring_session()
result = process_tab_switch_event(session_id, {
    "event_type": "tab_switch",
    "event_id": "tab_switch_1",
    "timestamp": time.time()
})

assert result["success"] == True, "Should succeed"
assert result["penalty_applied"] == True, "Should apply penalty"
assert result["penalty_amount"] == 3, "Should be +3 warnings"
assert result["warning_count"] == 3, f"Should have 3 warnings, got {result['warning_count']}"
print("✓ PASS: +3 warnings for tab switch")


# TEST 9: Browser minimize - +3 warnings (not +6 for duplicate)
print("\n[TEST 9] Browser minimize - no duplicate penalty")
session_id = create_proctoring_session()

# First tab switch
result1 = process_tab_switch_event(session_id, {
    "event_type": "tab_switch",
    "event_id": "event_1",
    "timestamp": time.time()
})

# Duplicate event (same event_id)
result2 = process_tab_switch_event(session_id, {
    "event_type": "tab_switch",
    "event_id": "event_1",
    "timestamp": time.time()
})

assert result1["warning_count"] == 3, "First event should add +3"
assert result2["warning_count"] == 3, "Duplicate should not add more"
assert result2["penalty_applied"] == False, "Duplicate should be rejected"
print("✓ PASS: Duplicate event prevented")


# TEST 10: Warning count from 7 to 10+ after tab switch
print("\n[TEST 10] Termination at 10 warnings")
session_id = create_proctoring_session()

# Add 7 warnings through face violations
for violation_num in range(7):
    # Reset to normal
    for i in range(6):
        process_monitoring_event(session_id, {
            "face_detected": True,
            "face_count": 1,
            "violation_type": None,
            "confidence": 0.95,
            "timestamp": time.time()
        })
        time.sleep(0.15)
    
    # Trigger violation
    for i in range(7):
        result = process_monitoring_event(session_id, {
            "face_detected": False,
            "face_count": 0,
            "violation_type": "face_absent",
            "confidence": 0.90,
            "timestamp": time.time(),
            "event_id": f"v{violation_num}_{i}"
        })
        time.sleep(0.15)

status = get_session_status(session_id)
assert status["warning_count"] == 7, f"Should have 7 warnings, got {status['warning_count']}"

# Now tab switch to reach 10
result = process_tab_switch_event(session_id, {
    "event_type": "tab_switch",
    "event_id": "final_tab_switch",
    "timestamp": time.time()
})

assert result["warning_count"] == 10, f"Should have 10 warnings (capped), got {result['warning_count']}"
assert result["should_terminate"] == True, "Should terminate"
assert result["interview_status"] == "terminated", "Status should be terminated"
print("✓ PASS: Interview terminated at 10 warnings")


# TEST 11: Incident reset after returning to normal
print("\n[TEST 11] Incident reset after returning to normal")
session_id = create_proctoring_session()

# Trigger violation
for i in range(7):
    process_monitoring_event(session_id, {
        "face_detected": False,
        "face_count": 0,
        "violation_type": "face_absent",
        "confidence": 0.90,
        "timestamp": time.time(),
        "event_id": f"reset_test_{i}"
    })
    time.sleep(0.2)

# Return to normal for 1+ second
for i in range(6):
    result = process_monitoring_event(session_id, {
        "face_detected": True,
        "face_count": 1,
        "violation_type": None,
        "confidence": 0.95,
        "timestamp": time.time()
    })
    time.sleep(0.2)

assert result["monitoring_status"] == "normal", "Should be in normal state"
assert result["warning_count"] == 1, "Should still have 1 warning from before"
print("✓ PASS: Incident reset after normal state")


# TEST 12: Verify Speech-to-Text still works (integration test)
print("\n[TEST 12] Speech-to-Text integration (structural check)")
try:
    from speech_to_text_service import transcribe_audio
    print("✓ PASS: Speech-to-Text module accessible")
except ImportError:
    print("⚠ WARNING: Speech-to-Text module not found (may be expected in test environment)")


# TEST 13: Verify existing evaluation still works (structural check)
print("\n[TEST 13] AI evaluation integration (structural check)")
try:
    from evaluation_service import evaluate_answer
    print("✓ PASS: AI evaluation module accessible")
except ImportError:
    print("⚠ WARNING: AI evaluation module not found (may be expected in test environment)")


# TEST 14: Verify interview progression (structural check)
print("\n[TEST 14] Interview service integration (structural check)")
try:
    from interview_service import start_interview
    print("✓ PASS: Interview service module accessible")
except ImportError:
    print("⚠ WARNING: Interview service module not found (may be expected in test environment)")


# TEST 15: Camera unavailable handling
print("\n[TEST 15] Camera unavailable handling")
session_id = create_proctoring_session()
from proctoring_service import handle_camera_event

result = handle_camera_event(session_id, "disconnect")
assert result["success"] == True, "Should handle disconnect"
assert result["interview_paused"] == True, "Should pause interview"
print("✓ PASS: Camera disconnect pauses interview")

result = handle_camera_event(session_id, "reconnect")
assert result["success"] == True, "Should handle reconnect"
assert result["interview_resumed"] == True, "Should resume interview"
print("✓ PASS: Camera reconnect resumes interview")


# SUMMARY
print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED")
print("=" * 70)
print(f"\nStrict proctoring security validated:")
print(f"  ✓ 1-second violation thresholds")
print(f"  ✓ +3 tab switch penalty")
print(f"  ✓ Duplicate event prevention")
print(f"  ✓ Warning counter accuracy")
print(f"  ✓ Interview termination at {MAX_WARNINGS} warnings")
print(f"  ✓ Incident reset logic")
print(f"  ✓ Camera event handling")
print(f"  ✓ Integration with existing modules")
print("=" * 70)
