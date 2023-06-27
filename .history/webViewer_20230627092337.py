import cv2
from flask import Flask, render_template, Response, render_template_string
import os
import threading
import sys

class VideoStream:
    def __init__(self, port=5000):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            return render_template('index.html')

        self.port = port
        self.subpages = {}

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
    def checkKeyboardInput(videoStream):
        while True:
            input("press enter to stop ")
            videoStream.pause()
            input("press enter to start ")
            videoStream.unpause()

    cap = cv2.VideoCapture(-1)
    videoStream = VideoStream()

    # Start the keyboard input checking thread
    keyboard_thread = threading.Thread(target=checkKeyboardInput, args=(videoStream,))
    keyboard_thread.start()

    try:
        while True:
            _, frame = cap.read()
            videoStream.imshow("frame", frame)
    except Exception as e:
        print(e)
        sys.exit()
        
