import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from imutils.video import VideoStream
import os
import numpy as np
from app.dbms.person import PersonInfo, createPerson, person


class AddPerson(tk.Frame):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(main_frame, bg="#FFFFFF", width=1200, height=500, *args, **kwargs)
        self.video = None
        self.detect = False
        self.face_cascade = cv2.CascadeClassifier(
            '/Users/lvc/PycharmProjects/pythonProject4/haarcascade_frontalface_default.xml')
        self.face_id = None
        self.count = 0
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=1200, height=880, bg="white")

        self.id_label = ttk.Label(self, text="ID:")
        self.id_label.place(x=10, y=550)
        self.id_entry = ttk.Entry(self)
        self.id_entry.place(x=10, y=570)

        self.username_label = ttk.Label(self, text="Username:")
        self.username_label.place(x=300, y=550)
        self.username_entry = ttk.Entry(self)
        self.username_entry.place(x=300, y=570)

        self.age_label = ttk.Label(self, text="Age:")
        self.age_label.place(x=600, y=550)
        self.age_entry = ttk.Entry(self)
        self.age_entry.place(x=600, y=570)

        self.phone_label = ttk.Label(self, text="Phone:")
        self.phone_label.place(x=10, y=600)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.place(x=10, y=620)

        self.email_label = ttk.Label(self, text="Email:")
        self.email_label.place(x=300, y=600)
        self.email_entry = ttk.Entry(self)
        self.email_entry.place(x=300, y=620)

        self.address_label = ttk.Label(self, text="Address:")
        self.address_label.place(x=600, y=600)
        self.address_entry = ttk.Entry(self)
        self.address_entry.place(x=600, y=620)

        self.add_person_button = tk.Button(self, text="Add Person", command=self.add_person)
        self.add_person_button.place(x=850, y=850)

        self.start_stop_button = tk.Button(self, text="Start Camera", command=self.toggle_camera)
        self.start_stop_button.place(x=400, y=850)
        self.start_face_detection = tk.Button(self, text="Start Face Detection", command=self.start_face_detection)
        self.start_face_detection.place(x=200, y=850)

        self.capture_button = tk.Button(self, text="Capture Faces", command=self.capture_faces)
        self.capture_button.place(x=550, y=850)
        self.train_button = tk.Button(self, text="Train Recognizer", command=self.train_recognizer)
        self.train_button.place(x=700, y=850)

        self.canvas.pack()
        self.canvas.bind("<Button-1>")
        self.bind_all("<Key>")
        self.after(1, self.update_frame)

    def add_person(self):
        person_info = {
            'id': self.id_entry.get(),
            'username': self.username_entry.get(),
            'age': self.age_entry.get(),
            'phone': self.phone_entry.get(),
            'email': self.email_entry.get(),
            'address': self.address_entry.get()
        }

        # Create a new person in the database
        createPerson(person_info)
        print("Person added successfully.")

    def toggle_camera(self):
        if self.video is None:
            self.video = VideoStream(src=0).start()
            self.start_stop_button.config(text="Stop Camera")
        else:
            self.video.stop()
            self.video = None
            self.start_stop_button.config(text="Start Camera")

    def update_frame(self):
        if self.video is not None:
            frame = self.video.read()
            frame = cv2.flip(frame, 1)

            if self.detect:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Thay đổi kích thước của frame, ví dụ: giảm xuống 50%
            scaled_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

            self.photo = self.convert_frame_to_photo(scaled_frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.after(10, self.update_frame)

    def convert_frame_to_photo(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        return photo

    def start_face_detection(self):
        self.detect = True

    def stop_face_detection(self):
        self.detect = False

    def set_face_id(self, face_id):
        self.face_id = face_id

    def capture_faces(self):
        face_id = self.id_entry.get()  # Get the user id from the entry widget
        if face_id:
            user_input = self.id_entry.get()
            custom_suffix = user_input.strip()  # Remove leading/trailing whitespaces

            while self.count < 30:
                img = self.video.read()

                if img is None:
                    print("\n [ERROR] Failed to capture frame. Exiting...")
                    break

                img = cv2.flip(img, 1)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    self.count += 1
                    image_name = f"/Users/lvc/PycharmProjects/pythonProject4/dataset/User.{face_id}.{self.count}.jpg"

                    cv2.imwrite(image_name, gray[y:y + h, x:x + w])

                cv2.imshow('image', img)

                k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
                if k == 27 or self.count >= 30:
                    break

            self.count = 0
            print(f"\n [INFO] Captured 30 face samples for user {face_id}")
        else:
            print("Please enter a valid user id.")

    def train_recognizer(self):
        path = '/Users/lvc/PycharmProjects/pythonProject4/dataset'
        faces, ids = self.get_images_and_labels(path)
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.write('/Users/lvc/PycharmProjects/pythonProject4/trainer/trainer.yml')
        print("\n [INFO] Recognizer trained. Exiting Program")

    def get_images_and_labels(self, path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        face_samples = []
        ids = []

        for image_path in image_paths:
            pil_img = Image.open(image_path).convert('L')  # convert it to grayscale
            img_numpy = np.array(pil_img, 'uint8')
            id = int(os.path.split(image_path)[-1].split(".")[1])
            faces = self.face_cascade.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                face_samples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)

        return face_samples, ids




def addperson(main_frame):
    return AddPerson(main_frame)
