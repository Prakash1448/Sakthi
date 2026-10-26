"""
=========================================
Proctoring Service Test
AI Interview Platform
=========================================
"""

import time
from proctoring_service import (
    create_proctoring_session,
    process_monitoring_event,
    get_session_status,
    handle_camera_event,
    terminate_session,
    MAX_WARNINGS
)


def test_session_creation():
    """Test creating a proctoring session."""
    print("\n[TEST] Session Creation")
    session_id = create_proctoring_session()
    assert session_id is not None
    print(f"✓ Created session: {session_id[:8]}...")
    return session_id


def test_normal_detection(session_id):
    """Test normal detection (no violation)."""
    print("\n[TEST] Normal Detection")
    
    result = process_monitoring_event(session_id, {
        "face_detected": True,
        "face_count": 1,
        "violation_type": None,
        "confidence": 0.95,
        "timestamp": time.time()
    })
    
    assert result["success"] == True
    assert result["warning_issued"] == False
    assert result["monitoring_status"] == "normal"
    print("✓ Normal state detected correctly")


def test_short_violation(session_id):
    """Test that short violations don't trigger warnings."""
    print("\n[TEST] Short Violation (Should Not Warn)")
    
    # Simulate brief looking away (under threshold)
    for i in range(3):
        result = process_monitoring_event(session_id, {
            "face_detected": True,
            "face_count": 1,
            "violation_type": "looking_left",
            "confidence": 0.85,
            "timestamp": time.time()
        })
        time.sleep(0.5)
    
    # Return to normal before threshold
    result = process_monitoring_event(session_id, {
        "face_detected": True,
        "face_count": 1,
        "violation_type": None,
        "confidence": 0.95,
        "timestamp": time.time()
    })
    
    assert result["warning_count"] == 0
    print("✓ Short violation did not trigger warning")


def test_sustained_violation(session_id):
    """Test that sustained violations trigger warnings."""
    print("\n[TEST] Sustained Violation (Should Warn)")
    
    initial_warning_count = 0
    
    # Simulate sustained looking away (over threshold)
    for i in range(6):
        result = process_monitoring_event(session_id, {
            "face_detected": True,
            "face_count": 1,
            "violation_type": "looking_right",
            "confidence": 0.90,
            "timestamp": time.time()
        })
        time.sleep(0.7)
    
    assert result["warning_count"] > initial_warning_count
    assert result["warning_issued"] == True
    print(f"✓ Sustained violation triggered warning (count: {result['warning_count']})")
    
    return result["warning_count"]


def test_incident_reset(session_id):
    """Test that incidents reset after returning to normal."""
    print("\n[TEST] Incident Reset")
    
    # Return to normal for required duration
    for i in range(4):
        result = process_monitoring_event(session_id, {
            "face_detected": True,
            "face_count": 1,
            "violation_type": None,
            "confidence": 0.95,
            "timestamp": time.time()
        })
        time.sleep(0.6)
    
    assert result["monitoring_status"] == "normal"
    print("✓ Incident reset after sustained normal state")


def test_multiple_warnings(session_id, start_count):
    """Test multiple warnings accumulate."""
    print("\n[TEST] Multiple Warnings")
    
    # Trigger another warning with different violation type
    for i in range(6):
        result = process_monitoring_event(session_id, {
            "face_detected": False,
            "face_count": 0,
            "violation_type": "face_absent",
            "confidence": 0.90,
            "timestamp": time.time()
        })
        time.sleep(0.7)
    
    assert result["warning_count"] > start_count
    print(f"✓ Multiple warnings accumulated (count: {result['warning_count']})")
    
    return result["warning_count"]


def test_multiple_faces(session_id, current_count):
    """Test multiple face detection."""
    print("\n[TEST] Multiple Faces Detection")
    
    # Reset to normal first
    for i in range(4):
        process_monitoring_event(session_id, {
            "face_detected": True,
            "face_count": 1,
            "violation_type": None,
            "confidence": 0.95,
            "timestamp": time.time()
        })
        time.sleep(0.6)
    
    # Simulate multiple faces
    for i in range(6):
        result = process_monitoring_event(session_id, {
            "face_detected": True,
            "face_count": 2,
            "violation_type": "multiple_faces",
            "confidence": 0.80,
            "timestamp": time.time()
        })
        time.sleep(0.7)
    
    assert result["warning_count"] > current_count
    print(f"✓ Multiple faces triggered warning (count: {result['warning_count']})")
    
    return result["warning_count"]


def test_camera_disconnect(session_id):
    """Test camera disconnection handling."""
    print("\n[TEST] Camera Disconnect")
    
    result = handle_camera_event(session_id, "disconnect")
    
    assert result["success"] == True
    assert result["status"] == "camera_disconnected"
    assert result["interview_paused"] == True
    print("✓ Camera disconnect handled correctly")


def test_camera_reconnect(session_id):
    """Test camera reconnection handling."""
    print("\n[TEST] Camera Reconnect")
    
    result = handle_camera_event(session_id, "reconnect")
    
    assert result["success"] == True
    assert result["status"] == "camera_reconnected"
    assert result["interview_resumed"] == True
    print("✓ Camera reconnect handled correctly")


def test_session_status(session_id):
    """Test getting session status."""
    print("\n[TEST] Session Status Retrieval")
    
    result = get_session_status(session_id)
    
    assert result["success"] == True
    assert "warning_count" in result
    assert "monitoring_status" in result
    assert "interview_status" in result
    print(f"✓ Session status retrieved (warnings: {result['warning_count']}/{MAX_WARNINGS})")


def test_warning_limit():
    """Test that 10 warnings terminates interview."""
    print("\n[TEST] Warning Limit and Termination")
    
    # Create new session for this test
    session_id = create_proctoring_session()
    
    # Trigger warnings until limit
    for warning_num in range(MAX_WARNINGS):
        # Reset to normal between violations
        for i in range(3):
            process_monitoring_event(session_id, {
                "face_detected": True,
                "face_count": 1,
                "violation_type": None,
                "confidence": 0.95,
                "timestamp": time.time()
            })
            time.sleep(0.3)
        
        # Trigger sustained violation
        for i in range(6):
            result = process_monitoring_event(session_id, {
                "face_detected": True,
                "face_count": 1,
                "violation_type": "looking_down",
                "confidence": 0.85,
                "timestamp": time.time()
            })
            time.sleep(0.7)
        
        print(f"  Warning {result['warning_count']}/{MAX_WARNINGS}")
        
        if warning_num == MAX_WARNINGS - 1:
            assert result["should_terminate"] == True
            assert result["interview_status"] == "terminated"
            print(f"✓ Interview terminated at {MAX_WARNINGS} warnings")
            break


def test_low_confidence_ignored(session_id):
    """Test that low confidence detections are ignored."""
    print("\n[TEST] Low Confidence Detections Ignored")
    
    initial_count = get_session_status(session_id)["warning_count"]
    
    # Send low confidence violations
    for i in range(10):
        result = process_monitoring_event(session_id, {
            "face_detected": True,
            "face_count": 1,
            "violation_type": "looking_left",
            "confidence": 0.3,  # Low confidence
            "timestamp": time.time()
        })
        time.sleep(0.5)
    
    final_count = result["warning_count"]
    assert final_count == initial_count
    print("✓ Low confidence detections ignored correctly")


def run_all_tests():
    """Run all proctoring service tests."""
    print("=" * 60)
    print("PROCTORING SERVICE - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    try:
        # Test 1: Session Creation
        session_id = test_session_creation()
        
        # Test 2: Normal Detection
        test_normal_detection(session_id)
        
        # Test 3: Short Violation (No Warning)
        test_short_violation(session_id)
        
        # Test 4: Sustained Violation (Warning)
        warning_count = test_sustained_violation(session_id)
        
        # Test 5: Incident Reset
        test_incident_reset(session_id)
        
        # Test 6: Multiple Warnings
        warning_count = test_multiple_warnings(session_id, warning_count)
        
        # Test 7: Multiple Faces
        warning_count = test_multiple_faces(session_id, warning_count)
        
        # Test 8: Camera Disconnect
        test_camera_disconnect(session_id)
        
        # Test 9: Camera Reconnect
        test_camera_reconnect(session_id)
        
        # Test 10: Session Status
        test_session_status(session_id)
        
        # Test 11: Low Confidence Ignored
        test_low_confidence_ignored(create_proctoring_session())
        
        # Test 12: Warning Limit
        test_warning_limit()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print(f"\nProctoring service is functioning correctly.")
        print(f"- Session creation: ✓")
        print(f"- Normal detection: ✓")
        print(f"- Violation detection: ✓")
        print(f"- Warning system: ✓")
        print(f"- Incident management: ✓")
        print(f"- Camera events: ✓")
        print(f"- Termination at {MAX_WARNINGS} warnings: ✓")
        print("=" * 60)
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
