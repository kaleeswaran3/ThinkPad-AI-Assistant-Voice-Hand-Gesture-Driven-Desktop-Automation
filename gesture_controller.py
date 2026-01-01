import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import math
from collections import deque
import platform

# --- Configuration & Constants ---
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SMOOTHING_BUFFER_SIZE = 5      # Number of frames to average for mouse movement
GESTURE_COOLDOWN_SECONDS = 0.5 # Cooldown between discrete actions (e.g. volume change)
CLICK_COOLDOWN_SECONDS = 1.0   # Cooldown for clicks to prevent double-clicks
SCROLL_SPEED = 30
MOUSE_SENSITIVITY = 1.5        # Multiplier for mouse movement speed

# MediaPipe constants
MP_HANDS = mp.solutions.hands
MP_DRAWING = mp.solutions.drawing_utils

class GestureController:
    def __init__(self):
        self.hands = MP_HANDS.Hands(
            static_image_mode=False,
            max_num_hands=1,  # Focus on one hand for control
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # State variables
        self.prev_time = 0
        self.last_action_time = 0
        self.last_click_time = 0
        self.current_gesture = "None"
        
        # Smoothing buffers
        self.cursor_queue = deque(maxlen=SMOOTHING_BUFFER_SIZE)
        
        # Mouse state
        self.is_dragging = False
        
        # For swipe detection (simple history of X positions)
        self.palm_x_history = deque(maxlen=10)
        
    def _get_distance(self, p1, p2):
        """Euclidean distance between two landmarks."""
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def _is_finger_up(self, landmarks, finger_tip_idx, finger_dip_idx):
        """Check if a finger is extended (Tip above DIP joint - Y is inverted in screen coords)."""
        return landmarks[finger_tip_idx].y < landmarks[finger_dip_idx].y

    def detect_gesture(self, landmarks):
        """
        Classify the hand gesture based on landmarks.
        Returns: gesture_name (str)
        """
        # Landmarks map:
        # 0: Wrist
        # 4: Thumb Tip, 8: Index Tip, 12: Middle Tip, 16: Ring Tip, 20: Pinky Tip
        # Joints needed for logic: 
        # Thumb: 4 (Tip), 3 (IP), 2 (MCP) -- Thumb logic is tricky, usually check x/y relative to palm
        # Index: 8 (Tip), 6 (PIP)
        # Middle: 12 (Tip), 10 (PIP)
        # Ring: 16 (Tip), 14 (PIP)
        # Pinky: 20 (Tip), 18 (PIP)

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        wrist = landmarks[0]
        
        # Fingers extended status
        # Note: simplistic check "y < y_lower_joint" works for upright hand. 
        # For more robustness in all angles, we'd need vector math, but this suffices for a "Webcam Control" usually held upright.
        index_up = index_tip.y < landmarks[6].y
        middle_up = middle_tip.y < landmarks[10].y
        ring_up = ring_tip.y < landmarks[14].y
        pinky_up = pinky_tip.y < landmarks[18].y
        
        # Thumb is defined differently (usually by x offset or distance from index base)
        # Simple check: Thumb tip is far from pinky base
        # thumb_up = thumb_tip.y < landmarks[3].y # Can be unreliable if hand is tilted
        
        # Count raised fingers (excluding thumb for now to keep it simple)
        raised_fingers = sum([index_up, middle_up, ring_up, pinky_up])
        
        # --- Gesture Logic ---
        
        # 1. FIST (Stop / Idle)
        # All fingers curled down
        if raised_fingers == 0:
            # Check thumb position to confirm strict fist or just closed hand
            return "Fist"

        # 2. OPEN PALM (Pause / Reset)
        # All fingers up
        if raised_fingers == 4:
            # Check if thumb is also "out" (approx)
            return "Open Palm"

        # 3. PINCH (Drag)
        # Index and Thumb tips are very close
        dist_thumb_index = self._get_distance(thumb_tip, index_tip)
        if dist_thumb_index < 0.05: # Threshold is percentage of screen, tune if needed
            return "Pinch"

        # 4. TWO FINGERS (Left Click / Peace Sign)
        if index_up and middle_up and not ring_up and not pinky_up:
            return "Two Fingers"
            
        # 5. INDEX POINTING (Mouse Move)
        if index_up and not middle_up and not ring_up and not pinky_up:
            return "Index Pointing"

        # 6. THUMBS UP / DOWN
        # Fingers are curled (like fist) but thumb is extended
        if raised_fingers == 0: # Checks strictly curled fingers
             # Thumb y comparison vs Wrist y
             # Y increases downwards. 
             # Thumb Up: Thumb Tip Y < Wrist Y (significantly)
             # Thumb Down: Thumb Tip Y > Wrist Y
             if thumb_tip.y < wrist.y - 0.1: # Threshold
                 return "Thumb Up"
             if thumb_tip.y > wrist.y + 0.1:
                 return "Thumb Down"
        
        # 7. SWIPE (Movement based, returns special state or handled in history)
        # (This is better handled by tracking wrist movement over frames, not static)

        return "Unknown"

    def process_frame(self, frame, mirror=True):
        """
        Main processing function.
        Args:
            frame: OpenCV BGR frame.
            mirror: Whether to flip the frame horizontally (default True for webcam).
        Returns:
            processed_frame: Frame with overlays.
            gesture_info: Dict with 'name', 'action'.
        """
        if mirror:
            frame = cv2.flip(frame, 1)
            
        frame_h, frame_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        action_taken = None
        gesture_name = "None"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                MP_DRAWING.draw_landmarks(frame, hand_landmarks, MP_HANDS.HAND_CONNECTIONS)
                
                # Detect Gesture
                gesture_name = self.detect_gesture(hand_landmarks.landmark)
                self.current_gesture = gesture_name
                
                # Execute Logic based on Gesture
                action_taken = self._handle_gesture_action(gesture_name, hand_landmarks, frame_w, frame_h)
                
                # Handle Swipe Logic (independent of static pose usually, but here tied to Open Palm)
                if gesture_name == "Open Palm":
                    self._handle_swipe(hand_landmarks.landmark[0].x) # Track wrist X
                else:
                    self.palm_x_history.clear()

        else:
            self.current_gesture = "None"
            self.palm_x_history.clear()
            
        # Overlay Info
        cv2.putText(frame, f"Gesture: {gesture_name}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if action_taken:
            cv2.putText(frame, f"Action: {action_taken}", (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
        return frame, gesture_name

    def _handle_gesture_action(self, gesture, landmarks, frame_w, frame_h):
        """Execute system commands logic with cooldowns."""
        current_time = time.time()
        
        # --- 1. MOUSE MOVE (Index Pointing) ---
        if gesture == "Index Pointing":
            # Map index finger tip to screen
            tip = landmarks.landmark[8]
            
            # Use a smaller active area for better reachability
            # e.g. Box in center of frame 20% to 80%
            margin = 0.2
            x = np.clip(tip.x, margin, 1 - margin)
            y = np.clip(tip.y, margin, 1 - margin)
            
            # Normalize to 0-1
            x = (x - margin) / (1 - 2 * margin)
            y = (y - margin) / (1 - 2 * margin)
            
            screen_x = int(x * SCREEN_WIDTH)
            screen_y = int(y * SCREEN_HEIGHT)
            
            # Smooth
            self.cursor_queue.append((screen_x, screen_y))
            avg_x = int(sum(c[0] for c in self.cursor_queue) / len(self.cursor_queue))
            avg_y = int(sum(c[1] for c in self.cursor_queue) / len(self.cursor_queue))
            
            pyautogui.moveTo(avg_x, avg_y)
            return "Moving Mouse"

        # --- 2. LEFT CLICK (Two Fingers) ---
        if gesture == "Two Fingers":
            if current_time - self.last_click_time > CLICK_COOLDOWN_SECONDS:
                pyautogui.click()
                self.last_click_time = current_time
                return "Left Click"
            return "Click Cooldown"

        # --- 3. DRAG (Pinch) ---
        if gesture == "Pinch":
            if not self.is_dragging:
                pyautogui.mouseDown()
                self.is_dragging = True
            
            # Move while dragging (same logic as Index Pointing but using midpoint of pinch)
            # Or just use Index tip for simplicity
            tip = landmarks.landmark[8]
            screen_x = int(tip.x * SCREEN_WIDTH)
            screen_y = int(tip.y * SCREEN_HEIGHT)
            pyautogui.moveTo(screen_x, screen_y)
            return "Dragging"
        else:
            if self.is_dragging:
                pyautogui.mouseUp()
                self.is_dragging = False

        # --- 4. VOLUME CONTROL (Thumbs) ---
        if gesture == "Thumb Up":
            if current_time - self.last_action_time > 0.2: # Fast repeat
                pyautogui.press("volumeup")
                self.last_action_time = current_time
                return "Volume Up"
        
        if gesture == "Thumb Down":
            if current_time - self.last_action_time > 0.2:
                pyautogui.press("volumedown")
                self.last_action_time = current_time
                return "Volume Down"

        # --- 5. STOP / IDLE (Fist) ---
        if gesture == "Fist":
             # Optional: Could lock the system or just do nothing
             return "Stopped"

        return None

    def _handle_swipe(self, current_x):
        """Simple history-based swipe detection for Open Palm."""
        self.palm_x_history.append(current_x)
        if len(self.palm_x_history) < 3:
            return

        # Check net movement over last few frames
        start_x = self.palm_x_history[0]
        end_x = self.palm_x_history[-1]
        delta = end_x - start_x
        
        current_time = time.time()
        
        if abs(delta) > 0.15 and (current_time - self.last_action_time > GESTURE_COOLDOWN_SECONDS):
            if delta > 0: # Moving Right (flipped frame means actual hand went Left relative to camera user?)
                # Note: Frame is mirrored. 
                # If User moves hand Left -> Camera sees Right -> x increases.
                # So "delta > 0" is technically "Swipe Right" in the *image*, which is User's "Swipe Left" (Next Tab?).
                # Let's map delta > 0 to "Next" (Swipe Right in air)
                pyautogui.hotkey('ctrl', 'tab')
                print("Swipe Right detected -> Next Tab")
            else:
                pyautogui.hotkey('ctrl', 'shift', 'tab')
                print("Swipe Left detected -> Prev Tab")
            
            self.last_action_time = current_time
            self.palm_x_history.clear() # Reset to prevent double swipe

    def release(self):
        self.hands.close()

if __name__ == "__main__":
    # Test harness
    print("Starting Gesture Controller Test...")
    gc = GestureController()
    cap = cv2.VideoCapture(0)
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            processed, name = gc.process_frame(frame)
            cv2.imshow("Gesture Control Test", processed)
            
            if cv2.waitKey(5) & 0xFF == 27: # ESC
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        gc.release()
