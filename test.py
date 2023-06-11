import cv2
from flask import Flask, render_template, Response
import os
import threading
import sys

class VideoStream:
    def __init__(self):
        self.currentFolder = os.path.dirname(os.path.abspath(__file__))
        self.app = Flask(__name__, template_folder=self.currentFolder)
        self.frame=b""

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/video_feed')
        def video_feed():
            return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        self.run()

    def run(self):
        threading.Thread(target=self.app.run).start()

    def generate_frames(self):
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n')
    def imshow(self, frame):
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        self.frame = frame

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    videoStream = VideoStream()
    try:
        while True:
            _, frame = cap.read()
            videoStream.imshow(frame)
    except Exception as e:
        print(e)
        sys.exit()
        
