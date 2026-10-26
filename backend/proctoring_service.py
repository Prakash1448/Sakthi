"""
=========================================
Proctoring Service
AI Interview Platform
=========================================
Webcam-based interview monitoring with 10-warning system.
"""

import uuid
import time
from datetime import datetime
from typing import Dict, List, Optional

# In-memory session storage (no database dependency)
proctoring_sessions: Dict[str, Dict] = {}

# Configuration - STRICT SECURITY SETTINGS
MAX_WARNINGS = 10
FACE_ABSENCE_THRESHOLD = 1.0  # Strict: 1 second
HEAD_TURN_THRESHOLD = 1.0  # Strict: 1 second
LOOKING_DOWN_THRESHOLD = 1.0  # Strict: 1 second
MULTIPLE_FACE_THRESHOLD = 1.0  # Strict: 1 second
TAB_SWITCH_PENALTY = 3  # Browser tab switch: immediate +3 warnings
NORMAL_RESET_DURATION = 1.0  # Reset after 1 second normal


class ProctoringSession:
    """
    Manages proctoring state for a single interview session.
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.warning_count = 0
        self.current_violation_type = None
        self.violation_start_time = None
        self.last_normal_time = time.monotonic()  # Use monotonic time
        self.incident_active = False
        self.camera_status = "active"
        self.face_status = "detected"
        self.head_position = "normal"
        self.browser_status = "active"
        self.monitoring_status = "normal"
        self.interview_status = "active"
        self.events: List[Dict] = []
        self.created_at = datetime.now().isoformat()
        self.tab_switch_count = 0
        self.last_event_id = None  # Prevent duplicate events
        
    def to_dict(self):
        """Convert session to dictionary."""
        return {
            "session_id": self.session_id,
            "warning_count": self.warning_count,
            "current_violation_type": self.current_violation_type,
            "violation_start_time": self.violation_start_time,
            "last_normal_time": self.last_normal_time,
            "incident_active": self.incident_active,
            "camera_status": self.camera_status,
            "face_status": self.face_status,
            "head_position": self.head_position,
            "browser_status": self.browser_status,
            "monitoring_status": self.monitoring_status,
            "interview_status": self.interview_status,
            "warning_count_display": f"{min(self.warning_count, MAX_WARNINGS)}/{MAX_WARNINGS}",
            "created_at": self.created_at,
            "event_count": len(self.events)
        }
    
    def process_detection(self, detection_result: Dict) -> Dict:
        """
        Process detection result and update monitoring state.
        STRICT VERSION: 1-second thresholds for all violations.
        
        Args:
            detection_result: {
                "face_detected": bool,
                "face_count": int,
                "violation_type": str | None,
                "confidence": float,
                "timestamp": float,
                "event_id": str (optional, prevents duplicates)
            }
        
        Returns:
            {
                "warning_issued": bool,
                "warning_count": int,
                "warning_message": str | None,
                "monitoring_status": str,
                "interview_status": str,
                "should_terminate": bool
            }
        """
        
        current_time = time.monotonic()
        warning_issued = False
        warning_message = None
        should_terminate = False
        
        # Prevent duplicate events
        event_id = detection_result.get("event_id")
        if event_id and event_id == self.last_event_id:
            return {
                "warning_issued": False,
                "warning_count": min(self.warning_count, MAX_WARNINGS),
                "warning_message": None,
                "monitoring_status": self.monitoring_status,
                "interview_status": self.interview_status,
                "should_terminate": self.interview_status == "terminated"
            }
        
        if event_id:
            self.last_event_id = event_id
        
        # Check if interview is already terminated
        if self.interview_status == "terminated":
            return {
                "warning_issued": False,
                "warning_count": min(self.warning_count, MAX_WARNINGS),
                "warning_message": "Interview already terminated",
                "monitoring_status": "terminated",
                "interview_status": "terminated",
                "should_terminate": True
            }
        
        # Update camera and face status
        self.camera_status = "active" if detection_result.get("face_detected") is not None else "inactive"
        
        face_count = detection_result.get("face_count", 0)
        if face_count == 0:
            self.face_status = "not_detected"
        elif face_count == 1:
            self.face_status = "detected"
        else:
            self.face_status = f"multiple_detected ({face_count})"
        
        violation_type = detection_result.get("violation_type")
        confidence = detection_result.get("confidence", 0.0)
        
        # STRICT confidence threshold - only process VERY confident violations
        # This prevents false positives from normal face movements
        if confidence < 0.85:  # Very high threshold
            violation_type = None
        
        # Determine violation threshold based on type
        violation_threshold = self._get_violation_threshold(violation_type)
        
        # CASE 1: Normal state (no violation)
        if violation_type is None:
            self.last_normal_time = current_time
            self.monitoring_status = "normal"
            self.head_position = "normal"
            
            # Check if we need to reset incident state
            if self.incident_active:
                normal_duration = current_time - self.last_normal_time
                
                # Reset incident after sustained normal state (1 second)
                if normal_duration >= NORMAL_RESET_DURATION:
                    self.incident_active = False
                    self.current_violation_type = None
                    self.violation_start_time = None
            
            return {
                "warning_issued": False,
                "warning_count": min(self.warning_count, MAX_WARNINGS),
                "warning_message": None,
                "monitoring_status": self.monitoring_status,
                "interview_status": self.interview_status,
                "should_terminate": False
            }
        
        # CASE 2: Violation detected
        self.monitoring_status = "potential_violation"
        
        # Update head position display
        if violation_type in ["looking_left", "looking_right", "looking_down", "looking_up"]:
            self.head_position = violation_type.replace("_", " ")
        elif violation_type == "face_absent":
            self.head_position = "face not detected"
        elif violation_type == "multiple_faces":
            self.head_position = "multiple faces"
        
        # Check if this is a new incident or continuation
        if not self.incident_active or self.current_violation_type != violation_type:
            # New incident
            self.incident_active = True
            self.current_violation_type = violation_type
            self.violation_start_time = current_time
            
        else:
            # Continuing incident - check if duration threshold reached
            violation_duration = current_time - self.violation_start_time
            
            if violation_duration >= violation_threshold:
                # Issue warning (only once per incident)
                # Check we haven't already warned for this incident
                already_warned = False
                if len(self.events) > 0:
                    last_event = self.events[-1]
                    if (last_event.get("violation_type") == violation_type and 
                        current_time - last_event.get("monotonic_time", 0) < (violation_threshold + 1.0)):
                        already_warned = True
                
                if not already_warned:
                    self.warning_count += 1
                    warning_issued = True
                    
                    # Generate warning message
                    warning_message = self._generate_warning_message(violation_type)
                    
                    # Record event
                    event = {
                        "session_id": self.session_id,
                        "event_type": "warning",
                        "warning_number": self.warning_count,
                        "violation_type": violation_type,
                        "confidence": confidence,
                        "duration": violation_duration,
                        "timestamp": time.time(),
                        "monotonic_time": current_time,
                        "datetime": datetime.now().isoformat()
                    }
                    self.events.append(event)
                    
                    # Check if interview should terminate
                    if self.warning_count >= MAX_WARNINGS:
                        self.interview_status = "terminated"
                        self.monitoring_status = "terminated"
                        should_terminate = True
                        warning_message = self._generate_termination_message()
        
        return {
            "warning_issued": warning_issued,
            "warning_count": min(self.warning_count, MAX_WARNINGS),
            "warning_message": warning_message,
            "monitoring_status": self.monitoring_status,
            "interview_status": self.interview_status,
            "should_terminate": should_terminate
        }
    
    def _get_violation_threshold(self, violation_type: Optional[str]) -> float:
        """Get violation duration threshold based on type."""
        if violation_type == "face_absent":
            return FACE_ABSENCE_THRESHOLD
        elif violation_type in ["looking_left", "looking_right"]:
            return HEAD_TURN_THRESHOLD
        elif violation_type == "looking_down":
            return LOOKING_DOWN_THRESHOLD
        elif violation_type == "multiple_faces":
            return MULTIPLE_FACE_THRESHOLD
        return 1.0  # Default 1 second
    
    def process_tab_switch(self, event_data: Dict) -> Dict:
        """
        Process browser tab switch/visibility change event.
        Applies immediate +3 warning penalty.
        
        Args:
            event_data: {
                "event_type": "tab_switch" | "browser_minimize",
                "event_id": str (prevents duplicates),
                "timestamp": float
            }
        
        Returns:
            Warning response
        """
        # Prevent duplicate tab switch penalties
        event_id = event_data.get("event_id")
        if event_id and event_id == self.last_event_id:
            return {
                "warning_issued": False,
                "warning_count": min(self.warning_count, MAX_WARNINGS),
                "warning_message": None,
                "penalty_applied": False
            }
        
        if event_id:
            self.last_event_id = event_id
        
        # Check if already terminated
        if self.interview_status == "terminated":
            return {
                "warning_issued": False,
                "warning_count": min(self.warning_count, MAX_WARNINGS),
                "warning_message": "Interview already terminated",
                "penalty_applied": False
            }
        
        # Apply +3 penalty
        self.warning_count += TAB_SWITCH_PENALTY
        self.tab_switch_count += 1
        self.browser_status = "tab_switched"
        
        # Record event
        event = {
            "session_id": self.session_id,
            "event_type": "tab_switch_penalty",
            "warning_penalty": TAB_SWITCH_PENALTY,
            "new_warning_count": self.warning_count,
            "timestamp": time.time(),
            "monotonic_time": time.monotonic(),
            "datetime": datetime.now().isoformat()
        }
        self.events.append(event)
        
        # Generate warning message
        warning_message = (
            f"SECURITY WARNING\n\n"
            f"Browser tab switch detected.\n\n"
            f"Penalty: +{TAB_SWITCH_PENALTY} warnings.\n\n"
            f"Total warnings: {min(self.warning_count, MAX_WARNINGS)}/{MAX_WARNINGS}."
        )
        
        # Check termination
        should_terminate = False
        if self.warning_count >= MAX_WARNINGS:
            self.interview_status = "terminated"
            self.monitoring_status = "terminated"
            should_terminate = True
            warning_message = self._generate_termination_message()
        
        return {
            "warning_issued": True,
            "warning_count": min(self.warning_count, MAX_WARNINGS),
            "warning_message": warning_message,
            "penalty_applied": True,
            "penalty_amount": TAB_SWITCH_PENALTY,
            "monitoring_status": self.monitoring_status,
            "interview_status": self.interview_status,
            "should_terminate": should_terminate
        }
    
    def _generate_warning_message(self, violation_type: str) -> str:
        """Generate user-facing warning message."""
        
        messages = {
            "looking_left": "Looking away from the interview screen was detected. Please face the camera.",
            "looking_right": "Looking away from the interview screen was detected. Please face the camera.",
            "looking_down": "Looking down was detected. Please maintain eye contact with the camera.",
            "looking_up": "Looking away from the screen was detected. Please face the camera.",
            "face_absent": "Your face has not been visible for the configured duration. Please adjust your camera.",
            "multiple_faces": "Multiple faces detected. Please ensure only the candidate is visible."
        }
        
        base_message = messages.get(violation_type, "Monitoring violation detected.")
        
        if self.warning_count < MAX_WARNINGS - 1:
            return f"WARNING {self.warning_count}/{MAX_WARNINGS}\n\n{base_message}"
        elif self.warning_count == MAX_WARNINGS - 1:
            return f"WARNING {self.warning_count}/{MAX_WARNINGS}\n\nYou have reached {MAX_WARNINGS - 1} warnings. Another sustained violation will end your interview session."
        else:
            return self._generate_termination_message()
    
    def _generate_termination_message(self) -> str:
        """Generate termination message."""
        return (
            f"INTERVIEW SESSION ENDED\n\n"
            f"The automated monitoring system recorded {MAX_WARNINGS} warning incidents.\n\n"
            f"Your session has been stopped and flagged for review."
        )
    
    def handle_camera_disconnect(self) -> Dict:
        """Handle camera disconnection event."""
        self.camera_status = "disconnected"
        self.monitoring_status = "camera_disconnected"
        
        event = {
            "session_id": self.session_id,
            "event_type": "camera_disconnect",
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat()
        }
        self.events.append(event)
        
        return {
            "status": "camera_disconnected",
            "message": "Camera connection lost. Please reconnect your camera to continue.",
            "interview_paused": True
        }
    
    def handle_camera_reconnect(self) -> Dict:
        """Handle camera reconnection event."""
        self.camera_status = "active"
        
        if self.interview_status != "terminated":
            self.monitoring_status = "normal"
        
        event = {
            "session_id": self.session_id,
            "event_type": "camera_reconnect",
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat()
        }
        self.events.append(event)
        
        return {
            "status": "camera_reconnected",
            "message": "Camera reconnected successfully.",
            "interview_resumed": True
        }


# API Functions

def create_proctoring_session() -> str:
    """Create a new proctoring session."""
    session_id = str(uuid.uuid4())
    session = ProctoringSession(session_id)
    proctoring_sessions[session_id] = session
    return session_id


def get_session(session_id: str) -> Optional[ProctoringSession]:
    """Get proctoring session by ID."""
    return proctoring_sessions.get(session_id)


def process_monitoring_event(session_id: str, detection_result: Dict) -> Dict:
    """
    Process a monitoring event for a session.
    
    Args:
        session_id: Proctoring session ID
        detection_result: Detection data from frontend
    
    Returns:
        Response with warning info and status
    """
    session = get_session(session_id)
    
    if not session:
        return {
            "success": False,
            "error": "Session not found"
        }
    
    result = session.process_detection(detection_result)
    
    return {
        "success": True,
        "session_id": session_id,
        **result,
        "session_state": session.to_dict()
    }


def process_tab_switch_event(session_id: str, event_data: Dict) -> Dict:
    """
    Process a browser tab switch/visibility event.
    Applies immediate +3 warning penalty.
    
    Args:
        session_id: Proctoring session ID
        event_data: Event data with event_id to prevent duplicates
    
    Returns:
        Response with penalty info
    """
    session = get_session(session_id)
    
    if not session:
        return {
            "success": False,
            "error": "Session not found"
        }
    
    result = session.process_tab_switch(event_data)
    
    return {
        "success": True,
        "session_id": session_id,
        **result,
        "session_state": session.to_dict()
    }


def get_session_status(session_id: str) -> Dict:
    """Get current session status."""
    session = get_session(session_id)
    
    if not session:
        return {
            "success": False,
            "error": "Session not found"
        }
    
    return {
        "success": True,
        **session.to_dict()
    }


def handle_camera_event(session_id: str, event_type: str) -> Dict:
    """Handle camera connection events."""
    session = get_session(session_id)
    
    if not session:
        return {
            "success": False,
            "error": "Session not found"
        }
    
    if event_type == "disconnect":
        result = session.handle_camera_disconnect()
    elif event_type == "reconnect":
        result = session.handle_camera_reconnect()
    else:
        return {
            "success": False,
            "error": "Invalid event type"
        }
    
    return {
        "success": True,
        **result,
        "session_state": session.to_dict()
    }


def terminate_session(session_id: str, reason: str = "manual") -> Dict:
    """Manually terminate a session."""
    session = get_session(session_id)
    
    if not session:
        return {
            "success": False,
            "error": "Session not found"
        }
    
    session.interview_status = "terminated"
    session.monitoring_status = "terminated"
    
    event = {
        "session_id": session_id,
        "event_type": "manual_termination",
        "reason": reason,
        "timestamp": time.time(),
        "datetime": datetime.now().isoformat()
    }
    session.events.append(event)
    
    return {
        "success": True,
        "session_terminated": True,
        "session_state": session.to_dict()
    }


def delete_session(session_id: str) -> bool:
    """Delete a session (cleanup)."""
    if session_id in proctoring_sessions:
        del proctoring_sessions[session_id]
        return True
    return False


# Testing
if __name__ == "__main__":
    print("=" * 60)
    print("Proctoring Service Test")
    print("=" * 60)
    
    # Create session
    session_id = create_proctoring_session()
    print(f"\nCreated session: {session_id}")
    
    # Test normal detection
    result = process_monitoring_event(session_id, {
        "face_detected": True,
        "face_count": 1,
        "violation_type": None,
        "confidence": 0.95,
        "timestamp": time.time()
    })
    print(f"\nNormal state: {result['monitoring_status']}")
    
    # Test violation detection
    for i in range(5):
        time.sleep(0.7)
        result = process_monitoring_event(session_id, {
            "face_detected": True,
            "face_count": 1,
            "violation_type": "looking_left",
            "confidence": 0.90,
            "timestamp": time.time()
        })
    
    print(f"\nAfter sustained violation:")
    print(f"Warnings: {result['warning_count']}")
    print(f"Status: {result['monitoring_status']}")
    
    if result.get('warning_issued'):
        print(f"Message: {result['warning_message']}")
    
    print("\n✓ Proctoring service test complete")
