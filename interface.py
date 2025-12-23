# import sys
# import cv2
# import numpy as np
# import tensorflow as tf
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# from PyQt5.QtCore import QTimer
# from PyQt5.QtGui import QImage, QPixmap
# import pygame
# import threading
# import pyttsx3
# import time

# class ObstacleDetector(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Smart Obstacle Avoidance Assistant")
        
#         # Load model (ignore the warning for now)
#         self.model = tf.keras.models.load_model('final_project\\models\\obstacle_detector.h5')  # or your model name

#         self.cap = cv2.VideoCapture(0)

#         # Pygame beep
#         pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
#         self.beep_sound = pygame.mixer.Sound('final_project\\assets\\beep.mp3')

#         # TTS Engine - configure once
#         self.tts_engine = pyttsx3.init()
#         self.tts_engine.setProperty('rate', 150)
#         self.tts_engine.setProperty('volume', 1.0)

#         self.last_direction = ""
#         self.last_speak_time = 0  # To prevent speaking too frequently

#         # UI setup (same as before)
#         self.label = QLabel(self)
#         self.label.setScaledContents(True)
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         self.setLayout(layout)
#         self.resize(900, 700)

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(33)

#     def speak(self, text):
#         """Speak text safely with debounce (no rapid repeats)"""
#         current_time = time.time()
#         if text == self.last_direction and (current_time - self.last_speak_time) < 2.5:
#             return  # Avoid repeating the same direction too quickly

#         self.last_direction = text
#         self.last_speak_time = current_time

#         # Run speech in separate thread
#         def _speak():
#             self.tts_engine.say(text)
#             self.tts_engine.runAndWait()  # Blocks only this thread

#         threading.Thread(target=_speak, daemon=True).start()

#     def play_beep(self):
#         threading.Thread(target=self.beep_sound.play, daemon=True).start()

#     def predict_zone(self, zone_img):
#         img = cv2.resize(zone_img, (128, 128))
#         img_norm = np.expand_dims(img / 255.0, axis=0)
#         logit = self.model.predict(img_norm, verbose=0)[0][0]
#         prob = tf.nn.sigmoid(logit).numpy()  # If you used from_logits=True in training
#         return prob > 0.5

#     def update_frame(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             return

#         h, w, _ = frame.shape

#         # Zones
#         left_zone = frame[:, :int(0.3 * w)]
#         middle_zone = frame[:, int(0.3 * w):int(0.7 * w)]
#         right_zone = frame[:, int(0.7 * w):]

#         left_obstacle = self.predict_zone(left_zone)
#         middle_obstacle = self.predict_zone(middle_zone)
#         right_obstacle = self.predict_zone(right_zone)

#         # Draw zones (same as before)
#         cv2.rectangle(frame, (0, 0), (int(0.3*w), h), (255, 255, 0), 3)
#         cv2.rectangle(frame, (int(0.3*w), 0), (int(0.7*w), h), (0, 255, 255), 3)
#         cv2.rectangle(frame, (int(0.7*w), 0), (w, h), (255, 255, 0), 3)
#         cv2.putText(frame, "LEFT", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
#         cv2.putText(frame, "MIDDLE", (int(0.35*w), 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
#         cv2.putText(frame, "RIGHT", (int(0.75*w), 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

#         status_text = "Clear Path Ahead"
#         status_color = (0, 255, 0)

#         if middle_obstacle:
#             self.play_beep()

#             if not left_obstacle and not right_obstacle:
#                 direction = "Go straight carefully"
#             elif not left_obstacle:
#                 direction = "Go Left"
#             elif not right_obstacle:
#                 direction = "Go Right"
#             else:
#                 direction = "Stop - obstacles on both sides"

#             self.speak(direction)
#             status_text = direction
#             status_color = (0, 0, 255)
#         else:
#             self.speak("")  # No need to speak anything

#         cv2.putText(frame, status_text, (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, status_color, 3)

#         # Display frame
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         q_img = QImage(frame_rgb.data, w, h, w * 3, QImage.Format_RGB888)
#         self.label.setPixmap(QPixmap.fromImage(q_img))

#     def closeEvent(self, event):
#         self.cap.release()
#         pygame.mixer.quit()
#         self.tts_engine.stop()
#         event.accept()

# def update_frame(self):
#     ret, frame = self.cap.read()
#     if not ret:
#         return

#     h, w, _ = frame.shape

#     # Define zone slices
#     left_zone = frame[:, :int(0.3 * w)]
#     middle_zone = frame[:, int(0.3 * w):int(0.7 * w)]
#     right_zone = frame[:, int(0.7 * w):]

#     # Predictions
#     left_obstacle = self.predict_zone(left_zone)
#     middle_obstacle = self.predict_zone(middle_zone)
#     right_obstacle = self.predict_zone(right_zone)

#     # Draw bounding boxes (full zone rectangles)
#     # Left zone
#     color_left = (0, 0, 255) if left_obstacle else (0, 255, 0)  # Red if obstacle, Green if clear
#     thickness_left = 6 if left_obstacle else 3
#     cv2.rectangle(frame, (0, 0), (int(0.3*w), h), color_left, thickness_left)

#     # Middle zone
#     color_middle = (0, 0, 255) if middle_obstacle else (0, 255, 0)
#     thickness_middle = 8 if middle_obstacle else 3  # Thicker for emphasis
#     cv2.rectangle(frame, (int(0.3*w), 0), (int(0.7*w), h), color_middle, thickness_middle)

#     # Right zone
#     color_right = (0, 0, 255) if right_obstacle else (0, 255, 0)
#     thickness_right = 6 if right_obstacle else 3
#     cv2.rectangle(frame, (int(0.7*w), 0), (w, h), color_right, thickness_right)

#     # Labels for zones
#     cv2.putText(frame, "LEFT", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_left, 3)
#     cv2.putText(frame, "MIDDLE", (int(0.35*w), 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color_middle, 4)
#     cv2.putText(frame, "RIGHT", (int(0.75*w), 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_right, 3)

#     # Guidance logic (same as before)
#     status_text = "Clear Path Ahead"
#     status_color = (0, 255, 0)

#     if middle_obstacle:
#         self.play_beep()

#         if not left_obstacle and not right_obstacle:
#             direction = "Go straight carefully"
#         elif not left_obstacle:
#             direction = "Go Left"
#         elif not right_obstacle:
#             direction = "Go Right"
#         else:
#             direction = "Stop - obstacles on both sides"

#         self.speak(direction)
#         status_text = direction
#         status_color = (0, 0, 255)
#     else:
#         self.speak("")  # Optional: clear previous speech if needed

#     cv2.putText(frame, status_text, (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.4, status_color, 4)

#     # Display the frame in GUI
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     q_img = QImage(frame_rgb.data, w, h, w * 3, QImage.Format_RGB888)
#     self.label.setPixmap(QPixmap.fromImage(q_img))

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ObstacleDetector()
#     window.show()
#     sys.exit(app.exec_())

import sys
import cv2
import numpy as np
import tensorflow as tf
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QComboBox, QPushButton
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import pygame
import threading
import pyttsx3
import time

class ObstacleDetector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Obstacle Avoidance Assistant - Multi-Camera")
        self.current_camera_index = 0
        self.cap = None  # Will be initialized after selecting camera

        # Load model
        self.model = tf.keras.models.load_model('final_project\\models\\obstacle_detector_fixed.h5')

        # Pygame beep
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.beep_sound = pygame.mixer.Sound('final_project\\assets\\beep.mp3')

        # TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.last_direction = ""
        self.last_speak_time = 0

        # === UI Layout ===
        main_layout = QVBoxLayout()

        # Top control panel
        control_panel = QHBoxLayout()

        self.camera_combo = QComboBox()
        self.camera_combo.addItem("Select Camera...")
        self.camera_combo.currentIndexChanged.connect(self.switch_camera)

        self.refresh_btn = QPushButton("Refresh Cameras")
        self.refresh_btn.clicked.connect(self.refresh_camera_list)

        control_panel.addWidget(QLabel("Camera:"))
        control_panel.addWidget(self.camera_combo)
        control_panel.addWidget(self.refresh_btn)
        control_panel.addStretch()

        main_layout.addLayout(control_panel)

        # Video display
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        main_layout.addWidget(self.label)

        self.setLayout(main_layout)
        self.resize(1000, 700)

        # Timer for frame update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Initial camera scan and start
        self.refresh_camera_list()
        self.timer.start(33)

    def refresh_camera_list(self):
        """Scan for available cameras and update dropdown"""
        self.camera_combo.blockSignals(True)  # Prevent triggering switch during refresh
        self.camera_combo.clear()
        self.camera_combo.addItem("Select Camera...")

        available_cameras = []
        for i in range(10):  # Check first 10 indices
            cap_temp = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # CAP_DSHOW for Windows stability
            if cap_temp.isOpened():
                ret, _ = cap_temp.read()
                if ret:
                    available_cameras.append(i)
                cap_temp.release()

        if not available_cameras:
            self.camera_combo.addItem("No camera detected")
            self.label.setText("No camera found!")
            return

        for idx in available_cameras:
            self.camera_combo.addItem(f"Camera {idx}")

        # Try to re-select current one, or default to first
        if self.current_camera_index in available_cameras:
            index = available_cameras.index(self.current_camera_index) + 1  # +1 because of "Select..."
            self.camera_combo.setCurrentIndex(index)
        else:
            self.camera_combo.setCurrentIndex(1)  # First available
            self.current_camera_index = available_cameras[0]

        self.camera_combo.blockSignals(False)
        self.switch_camera()  # Open the selected one

    def switch_camera(self):
        """Switch to the selected camera index"""
        index = self.camera_combo.currentIndex()
        if index <= 0:
            return  # "Select Camera..." selected

        new_index = index - 1  # Because of offset from placeholder
        actual_index = self.get_available_camera_index(new_index)

        if actual_index is None:
            return

        # Release old camera
        if self.cap is not None:
            self.cap.release()

        # Open new one
        self.cap = cv2.VideoCapture(actual_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.label.setText(f"Failed to open Camera {actual_index}")
            return

        self.current_camera_index = actual_index
        print(f"Switched to Camera {actual_index}")

    def get_available_camera_index(self, combo_offset):
        """Helper to get real camera index from combo box"""
        count = 0
        for i in range(10):
            cap_temp = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap_temp.isOpened():
                ret, _ = cap_temp.read()
                cap_temp.release()
                if ret:
                    if count == combo_offset:
                        return i
                    count += 1
        return None

    def speak(self, text):
        current_time = time.time()
        if text == self.last_direction and (current_time - self.last_speak_time) < 2:
            return

        self.last_direction = text
        self.last_speak_time = current_time

        def _speak():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

        threading.Thread(target=_speak, daemon=True).start()

    def play_beep(self):
        threading.Thread(target=self.beep_sound.play, daemon=True).start()
        self.beep_sound.set_volume(0)

    def predict_zone(self, zone_img):
        if zone_img.size == 0:
            return False
        img = cv2.resize(zone_img, (128, 128))
        img_norm = np.expand_dims(img / 255.0, axis=0)
        logit = self.model.predict(img_norm, verbose=0)[0][0]
        prob = tf.nn.sigmoid(logit).numpy()
        return prob > 0.5

    # def update_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            self.label.setText("Camera disconnected!")
            return

        h, w, _ = frame.shape

        # Zones
        left_zone = frame[:, :int(0.3 * w)]
        middle_zone = frame[:, int(0.3 * w):int(0.7 * w)]
        right_zone = frame[:, int(0.7 * w):]

        left_obstacle = self.predict_zone(left_zone)
        middle_obstacle = self.predict_zone(middle_zone)
        right_obstacle = self.predict_zone(right_zone)

        # Draw zone borders with detection highlight
        color_left = (0, 0, 255) if left_obstacle else (0, 255, 0)
        thickness_left = 6 if left_obstacle else 3
        cv2.rectangle(frame, (0, 0), (int(0.3*w), h), color_left, thickness_left)

        color_middle = (0, 0, 255) if middle_obstacle else (0, 255, 0)
        thickness_middle = 8 if middle_obstacle else 3
        cv2.rectangle(frame, (int(0.3*w), 0), (int(0.7*w), h), color_middle, thickness_middle)

        color_right = (0, 0, 255) if right_obstacle else (0, 255, 0)
        thickness_right = 6 if right_obstacle else 3
        cv2.rectangle(frame, (int(0.7*w), 0), (w, h), color_right, thickness_right)

        # Zone labels
        cv2.putText(frame, "LEFT", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_left, 3)
        cv2.putText(frame, "MIDDLE", (int(0.35*w), 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color_middle, 4)
        cv2.putText(frame, "RIGHT", (int(0.75*w), 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_right, 3)

        # Guidance
        status_text = "Clear Path Ahead"
        status_color = (0, 255, 0)

        if middle_obstacle:
            self.play_beep()
            if not left_obstacle and not right_obstacle:
                direction = "Go straight carefully"
            elif not left_obstacle:
                direction = "Go Left"
            elif not right_obstacle:
                direction = "Go Right"
            else:
                direction = "Stop - obstacles on both sides"

            self.speak(direction)
            status_text = direction
            status_color = (0, 0, 255)

        cv2.putText(frame, status_text, (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.4, status_color, 4)

        # Show current camera info
        cv2.putText(frame, f"Camera {self.current_camera_index}", (w - 200, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Display in GUI
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        q_img = QImage(frame_rgb.data, w, h, w * 3, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_img))

    def update_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            self.label.setText("Camera disconnected!")
            return

        h, w, _ = frame.shape

        # Updated zones: Left 40%, Middle 20%, Right 40%
        left_zone = frame[:, :int(0.4 * w)]
        middle_zone = frame[:, int(0.4 * w):int(0.6 * w)]
        right_zone = frame[:, int(0.6 * w):]

        left_obstacle = self.predict_zone(left_zone)
        middle_obstacle = self.predict_zone(middle_zone)
        right_obstacle = self.predict_zone(right_zone)

        # Draw zone borders with detection highlight
        color_left = (0, 0, 255) if left_obstacle else (0, 255, 0)
        thickness_left = 6 if left_obstacle else 3
        cv2.rectangle(frame, (0, 0), (int(0.4*w), h), color_left, thickness_left)

        color_middle = (0, 0, 255) if middle_obstacle else (0, 255, 0)
        thickness_middle = 8 if middle_obstacle else 3
        cv2.rectangle(frame, (int(0.4*w), 0), (int(0.6*w), h), color_middle, thickness_middle)

        color_right = (0, 0, 255) if right_obstacle else (0, 255, 0)
        thickness_right = 6 if right_obstacle else 3
        cv2.rectangle(frame, (int(0.6*w), 0), (w, h), color_right, thickness_right)

        # Zone labels (with optional percentages for debugging)
        cv2.putText(frame, "LEFT (40%)", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_left, 3)
        cv2.putText(frame, "MIDDLE (20%)", (int(0.45*w), 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color_middle, 4)
        cv2.putText(frame, "RIGHT (40%)", (int(0.65*w), 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_right, 3)

        # Guidance logic (unchanged)
        status_text = "Clear Path Ahead"
        status_color = (0, 255, 0)

        if middle_obstacle:
            self.play_beep()
            if not left_obstacle and not right_obstacle:
                direction = "Go straight carefully"
            elif not left_obstacle:
                direction = "Go Left"
            elif not right_obstacle:
                direction = "Go Right"
            else:
                direction = "Stop - obstacles on both sides"

            self.speak(direction)
            status_text = direction
            status_color = (0, 0, 255)

        cv2.putText(frame, status_text, (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.4, status_color, 4)

        # Show current camera info
        cv2.putText(frame, f"Camera {self.current_camera_index}", (w - 200, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Display in GUI
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        q_img = QImage(frame_rgb.data, w, h, w * 3, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
        pygame.mixer.quit()
        self.tts_engine.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ObstacleDetector()
    window.show()
    sys.exit(app.exec_())