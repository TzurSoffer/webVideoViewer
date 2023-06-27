import cv2
from flask import Flask, render_template, Response, render_template_string
import os
import threading
import sys

class VideoStream:
    def __init__(self, port=5000):
        self.currentFolder = os.path.dirname(os.path.abspath(__file__))
        self.app = Flask(__name__, template_folder=self.currentFolder)


        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/videoFeed')
        def videoFeed():
            return Response(self.videoUpdater(), mimetype='multipart/x-mixed-replace; boundary=frame')

        self.port = port
        self.frame = b""
        self.running = True
        self.paused = False

    def run(self):
        threading.Thread(target=self.app.run, kwargs={"host": "0.0.0.0", "port": self.port}).start()

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def videoUpdater(self):
        while self.running:
            while not self.paused and self.running:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n')

    def imshow(self, name, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        self.videos[name] = frame

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    videoStream = VideoStream()

    try:
        while True:
            _, frame = cap.read()
            videoStream.imshow("frame", frame)
    except Exception as e:
        print(e)
        sys.exit()
        
