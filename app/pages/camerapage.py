import tkinter as tk
from imutils.video import VideoStream
import cv2
from PIL import Image, ImageTk
from app.dbms.person import PersonInfo, person, createPerson, RecognizedPerson, createRecognizedPerson
from datetime import datetime
from collections import defaultdict
import threading   # Import the datetime module for timestamp handling

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/Users/lvc/PycharmProjects/pythonProject4/trainer/trainer.yml')
cascadePath = "/Users/lvc/PycharmProjects/pythonProject4/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
id = 0

class CameraPage(tk.Frame):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(main_frame, bg="#FFFFFF", width=1200, height=500, *args, **kwargs)
        self.video = None
        self.create_widgets()
        self.detected_faces = set()
        self.last_update_time = defaultdict(datetime)

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=1200, height=880, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>")

        self.start_stop_button = tk.Button(self, text="Start Camera", command=self.toggle_camera)
        self.start_stop_button.pack(pady=10)

        self.bind_all("<Key>")
        self.after(1, self.update_frame)

    def toggle_camera(self):
        if self.video is None:
            self.video = VideoStream(src=0).start()
            self.start_stop_button.config(text="Stop Camera")
        else:
            self.video.stop()
            self.video = None
            self.start_stop_button.config(text="Start Camera")

    def update_frame(self):
        name = ""
        if self.video is not None:
            frame = self.video.read()
            frame = cv2.flip(frame, 1)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(0.1 * frame.shape[1]), int(0.1 * frame.shape[0])),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                recognized_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                print(f"Detected face with ID: {recognized_id}, confidence: {confidence}")

                if recognized_id not in self.detected_faces:
                    # New face detected, update the database
                    person_info = self.get_person_info(recognized_id)

                    if person_info:
                        name = f"{person_info.getUserName()} (ID: {person_info.getID()}, Age: {person_info.age})"
                        self.save_recognized_person(person_info.getID())
                        self.detected_faces.add(recognized_id)
                        self.last_update_time[recognized_id] = datetime.now()
                    else:
                        # Xử lý khi không tìm thấy thông tin
                        name = f"unknown (ID {recognized_id})"
                else:
                    # Face already detected, check if 10 minutes have passed for an update
                    last_recognition_time = self.last_update_time[recognized_id]
                    current_time = datetime.now()
                    if (current_time - last_recognition_time).total_seconds() >= 600:
                        person_info = self.get_person_info(recognized_id)

                        if person_info:

                            # Save recognized person to the database
                            self.save_recognized_person(person_info.getID())
                            # Update the last recognition time for this ID
                            self.last_update_time[recognized_id] = current_time
                        else:
                            # Xử lý khi không tìm thấy thông tin
                            name = f"unknown (ID {recognized_id})"

                person_info = self.get_person_info(recognized_id)
                name = f"{person_info.getUserName()} (ID: {person_info.getID()}, Age: {person_info.age})"
                confidence = "  {0}%".format(round(100 - confidence))
                cv2.putText(
                    frame,
                    name,
                    (x + 5, y - 5),
                    font,
                    1,
                    (255, 255, 255),
                    2
                )
                cv2.putText(
                    frame,
                    str(confidence),
                    (x + 5, y + h - 5),
                    font,
                    1,
                    (255, 255, 0),
                    1
                )

            self.photo = self.convert_frame_to_photo(frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.after(10, self.update_frame)



    def convert_frame_to_photo(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        return photo

    def get_person_info(self, recognized_id):
        # Lấy thông tin người dùng từ cơ sở dữ liệu
        person_info = person(PersonInfo(recognized_id, None, None, None, None, None))

        return PersonInfo(*person_info) if person_info else None

    def save_recognized_person(self, person_id):
        # Lưu thông tin người dùng vào cơ sở dữ liệu (RecognizedPersons table)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_recognized_person = createRecognizedPerson(RecognizedPerson(person_id, timestamp))

    def get_all_person_names(self):
        # Lấy danh sách tên người dùng từ cơ sở dữ liệu
        # Giả sử hàm get_all_person_names trả về danh sách tên từ cơ sở dữ liệu
        # Bạn cần sửa đổi hàm này tùy thuộc vào cấu trúc của cơ sở dữ liệu của bạn
        return ["unknown"] + [str(i) for i in range(1, 16)]  # Thay thế bằng hàm thích hợp

def camera_page(main_frame):
    return CameraPage(main_frame)
