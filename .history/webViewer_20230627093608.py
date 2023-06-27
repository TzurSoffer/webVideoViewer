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

        self.port = port
        self.subpages = {}
        self.run()

    def run(self):
        threading.Thread(target=self.app.run, kwargs={"host": "0.0.0.0", "port": self.port}).start()

    def add_subpage(self, subpage_name, html_template):
        self.subpages[subpage_name] = html_template

        @self.app.route('/' + subpage_name)
        def subpage():
            return render_template(self.subpages[subpage_name])

    def imshow(self, subpage_name, frame):
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        self.subpages[subpage_name] = frame

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
        
