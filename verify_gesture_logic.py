import unittest
from unittest.mock import MagicMock
from gesture_controller import GestureController

# Mock Landmark class
class MockLandmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TestGestureLogic(unittest.TestCase):
    def setUp(self):
        self.gc = GestureController()
        # Mock PyAutoGUI to prevent actual mouse movements during test
        self.cursor_origin = (0, 0)
    
    def create_hand(self, thumb_open=False, index_open=False, middle_open=False, ring_open=False, pinky_open=False):
        """Helper to create a list of landmarks representing a hand pose."""
        landmarks = [None] * 21
        
        # 0: Wrist at bottom center
        landmarks[0] = MockLandmark(0.5, 0.9)
        
        # Joints needed for logic:
        # Thumb: 4 (Tip), 3 (IP), 2 (MCP)
        # Index: 8 (Tip), 6 (PIP)
        # Middle: 12 (Tip), 10 (PIP)
        # Ring: 16 (Tip), 14 (PIP)
        # Pinky: 20 (Tip), 18 (PIP)
        
        # Base joints (MCPs/PIPs) - y position 0.6
        landmarks[3] = MockLandmark(0.4, 0.6)
        landmarks[6] = MockLandmark(0.5, 0.6)
        landmarks[10] = MockLandmark(0.5, 0.6)
        landmarks[14] = MockLandmark(0.5, 0.6)
        landmarks[18] = MockLandmark(0.5, 0.6)
        
        # Tips
        # Open finger tip y < joint y (e.g. 0.3 < 0.6)
        # Closed finger tip y > joint y (e.g. 0.8 > 0.6)
        
        # Thumb (Tip 4)
        if thumb_open:
            landmarks[4] = MockLandmark(0.8, 0.5) # Out to side
        else:
            landmarks[4] = MockLandmark(0.5, 0.7) # Tucked in
            
        # Index (Tip 8)
        landmarks[8] = MockLandmark(0.5, 0.3 if index_open else 0.8)
        
        # Middle (Tip 12)
        landmarks[12] = MockLandmark(0.5, 0.3 if middle_open else 0.8)
        
        # Ring (Tip 16)
        landmarks[16] = MockLandmark(0.5, 0.3 if ring_open else 0.8)
        
        # Pinky (Tip 20)
        landmarks[20] = MockLandmark(0.5, 0.3 if pinky_open else 0.8)
        
        return landmarks

    def test_fist(self):
        """Test detection of Fist (all fingers closed)."""
        landmarks = self.create_hand(thumb_open=False, index_open=False, middle_open=False, ring_open=False, pinky_open=False)
        gesture = self.gc.detect_gesture(landmarks)
        self.assertEqual(gesture, "Fist")

    def test_open_palm(self):
        """Test detection of Open Palm (all fingers open)."""
        landmarks = self.create_hand(thumb_open=True, index_open=True, middle_open=True, ring_open=True, pinky_open=True)
        gesture = self.gc.detect_gesture(landmarks)
        self.assertEqual(gesture, "Open Palm")

    def test_index_pointing(self):
        """Test Index Pointing (only index open)."""
        landmarks = self.create_hand(thumb_open=False, index_open=True, middle_open=False, ring_open=False, pinky_open=False)
        gesture = self.gc.detect_gesture(landmarks)
        self.assertEqual(gesture, "Index Pointing")
        
    def test_two_fingers(self):
        """Test Two Fingers / Peace Sign (Index & Middle)."""
        landmarks = self.create_hand(thumb_open=False, index_open=True, middle_open=True, ring_open=False, pinky_open=False)
        gesture = self.gc.detect_gesture(landmarks)
        self.assertEqual(gesture, "Two Fingers")

if __name__ == '__main__':
    unittest.main()
