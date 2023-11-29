import tkinter as tk
from imutils.video import VideoStream
from model.yolodetect import YoloDetect
import cv2
import numpy as np
from PIL import Image, ImageTk
import json

class IntrusionWarningPage(tk.Frame):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(main_frame, bg="#FFFFFF", width=1200, height=500, *args, **kwargs)
        self.points = []
        self.video = None
        self.model = YoloDetect()
        self.detect = False
        self.create_widgets()
        self.load_points_from_file()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=1200, height=880, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_left_click)

        self.start_stop_button = tk.Button(self, text="Start Camera", command=self.toggle_camera)
        self.start_stop_button.pack(pady=10)

        self.bind_all("<Key>", self.handle_key_event)
        self.after(1, self.update_frame)

    def toggle_camera(self):
        if self.video is None:
            self.video = VideoStream(src=0).start()
            self.start_stop_button.config(text="Stop Camera")
        else:
            self.video.stop()
            self.video = None
            self.start_stop_button.config(text="Start Camera")

    def handle_key_event(self, event):
        key = event.keysym
        if key == 'q':
            if self.video is not None:
                self.video.stop()
            self.save_points_to_file()  # Save points before closing the application
            self.destroy()
        elif key == 'd':
            self.detect = not self.detect
        elif key == 's':
            self.save_points_to_file()  # Save points when 's' key is pressed
        elif key == 'l':
            self.load_points_from_file()  # Load points when 'l' key is pressed

    def handle_left_click(self, event):
        x, y = event.x, event.y
        self.points.append([x, y])

    def clear_points(self):
        self.points = []

    def update_frame(self):
        if self.video is not None:
            frame = self.video.read()
            frame = cv2.flip(frame, 1)

            for point in self.points:
                frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)
            if len(self.points) > 1:
                frame = cv2.polylines(frame, [np.int32(self.points)], False, (255, 0, 0), thickness=2)

            if self.detect:
                frame = self.model.detect(frame=frame, points=self.points)

            self.photo = self.convert_frame_to_photo(frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.after(10, self.update_frame)

    def convert_frame_to_photo(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        return photo

    def save_points_to_file(self, filename="points.json"):
        with open(filename, "w") as file:
            json.dump(self.points, file)

    def load_points_from_file(self, filename="points.json"):
        try:
            with open(filename, "r") as file:
                self.points = json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found. No points loaded.")

def intrusion_warning_page(main_frame):
    return IntrusionWarningPage(main_frame)
