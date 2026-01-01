"""
Test script to verify camera and MediaPipe hand detection
Run this to diagnose issues with hand gesture detection
"""

import cv2
import mediapipe as mp

print("Testing camera and MediaPipe hand detection...")
print("=" * 50)

# Test 1: Check if camera opens
print("\n1. Testing camera access...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ ERROR: Could not open camera!")
    print("   - Check if another app is using the camera")
    print("   - Check camera permissions in Windows Settings")
    exit(1)
else:
    print("✓ Camera opened successfully")

# Test 2: Read a frame
print("\n2. Testing frame capture...")
ret, frame = cap.read()
if not ret:
    print("❌ ERROR: Could not read frame from camera!")
    cap.release()
    exit(1)
else:
    print(f"✓ Frame captured successfully (size: {frame.shape})")

# Test 3: Initialize MediaPipe
print("\n3. Testing MediaPipe Hands initialization...")
try:
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    print("✓ MediaPipe Hands initialized successfully")
except Exception as e:
    print(f"❌ ERROR: Failed to initialize MediaPipe: {e}")
    cap.release()
    exit(1)

# Test 4: Process a frame
print("\n4. Testing hand detection...")
print("   Show your hand to the camera for 5 seconds...")
print("   Press 'q' to quit early")

import time
start_time = time.time()
hand_detected = False

while time.time() - start_time < 5:
    ret, frame = cap.read()
    if not ret:
        continue
    
    # Flip and convert
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # Check for hands
    if results.multi_hand_landmarks:
        if not hand_detected:
            print("   ✓ Hand detected!")
            hand_detected = True
        
        # Draw landmarks on frame
        mp_drawing = mp.solutions.drawing_utils
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Show frame
    cv2.imshow('Hand Detection Test (Press Q to quit)', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()

print("\n" + "=" * 50)
if hand_detected:
    print("✓ ALL TESTS PASSED!")
    print("  Hand gesture detection should work in the main app.")
else:
    print("⚠ Camera and MediaPipe work, but no hand was detected.")
    print("  Make sure to show your hand clearly to the camera.")

print("\nTest complete. You can close this window.")
