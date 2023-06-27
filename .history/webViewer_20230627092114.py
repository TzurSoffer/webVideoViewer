import cv2
from flask import Flask, render_template, Response, render_template_string
import os
import threading
import sys

class VideoStream:
    def __init__(self, htmlTemplate="./index.html", port=5000):
        self.currentFolder = os.path.dirname(os.path.abspath(__file__))
        self.app = Flask(__name__, template_folder=self.currentFolder)
        self.frame=b""
        self.runing = True
        self.paused = False
        
        self.port = port

        @self.app.route('/')
        def index():
            return render_template(htmlTemplate)

        @self.app.route('/videoFeed')
        def videoFeed():
            return Response(self.videoUpdater(), mimetype='multipart/x-mixed-replace; boundary=frame')

        self.run()

    def run(self):
        threading.Thread(target=self.app.run, kwargs={"host": "0.0.0.0", "port": self.port}).start()
    
    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False
    
    def videoUpdater(self):
        while self.runing:
            while not self.paused and self.runing:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n')
    def imshow(self, frame):
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        self.frame = frame

        html = render_template_string('<img src="data:image/jpeg;base64,{{ frame }}" />', frame=frame)
        self.app.jinja_env.globals['frame'] = html
        self.app.jinja_env.globals['frame_name'] = subpage

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
        
