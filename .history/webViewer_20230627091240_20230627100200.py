import cv2
from flask import Flask, render_template, Response, render_template_string
import os
import threading
import sys

class VideoStream:
    def __init__(self, htmlTemplate="./index.html", port=5000):
        self.currentFolder = os.path.dirname(os.path.abspath(__file__))
        self.app = Flask(__name__, template_folder=self.currentFolder)
        self.videos = {}
        self.runing = True
        self.paused = False
        self.htmlTemplate = htmlTemplate
        
        self.port = port

        self.run()
        
    def _createTemplate(self, subpage):
        with open(self.htmlTemplate, "r") as f:
            template = str(f.read())
        template = template.replace("{videoFeed}", f"'{subpage}'")
        return(template)
    
    def _createSubpage(self, name):
        videoFeedName = f"{name}/videoFeed"
        template = self._createTemplate(videoFeedName)
        
        @self.app.route(f"/{name}")
        def index():
            return(render_template_string(template))

        @self.app.route(f"/{videoFeedName}")
        def videoFeed():
            return Response(self._videoUpdater(name), mimetype='multipart/x-mixed-replace; boundary=frame')

    def run(self):
        threading.Thread(target=self.app.run, kwargs={"host": "0.0.0.0", "port": self.port}).start()
    
    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False
    
    def _videoUpdater(self, subpage):
        while self.runing:
            while not self.paused and self.runing:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + self.videos.get(subpage, b"") + b'\r\n')
    
    def imshow(self, name, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        if name not in self.videos:
            self._createSubpage(name)
        
        self.videos[name] = frame

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
            videoStream.imshow(frame)
    except Exception as e:
        print(e)
        sys.exit()
        
