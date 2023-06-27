from flask import Flask, render_template, Response
import threading
import cv2
import os
import base64
import numpy as np

class SubpageManager:
    def __init__(self):
        self.frames = {}
    
    def imshow(self, name, frame):
        self.frames[name] = frame
    
    def getFrame(self, name):
        return self.frames.get(name, None)

class SubpageApp:
    def __init__(self, homePageTemplate="home.html", subpageTemplate="subpage.html", port=5000):
        self.currentFolder = os.path.dirname(os.path.abspath(__file__))
        self.app = Flask(__name__, template_folder=self.currentFolder)
        self.manager = SubpageManager()
        self.setupRoutes()
        self.homePageTemplate = homePageTemplate
        self.subpageTemplate = subpageTemplate
        self.subpages = []
        self.homePage = "<h1>Subpages for Names</h1><ul>{}</ul>"
    
    def setupRoutes(self):
        self.app.route('/')(self.index)
        self.app.route('/<name>')(self.subpage)
        self.app.route('/imshow/<name>')(self.imshow)
    
    def addSubpage(self, name):
        self.subpages.append(name)
    
    def index(self):
        subpages = ''.join(f'<li><a href="/{name}">{name}</a></li>' for name in self.subpages)
        return self.homePage.format(subpages)
    
    def subpage(self, name):
        def generate_frames():
            while True:
                frame = self.manager.getFrame(name)
                if frame is None:
                    yield Response(f'<h1>No subpage found for {name}</h1>'.encode('utf-8'), mimetype='text/html')
                else:
                    html_content = f'<img src="data:image/jpeg;base64,{frame.decode()}" alt="Video Feed" />'
                    yield Response(html_content.encode('utf-8'), mimetype='text/html')

        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    def imshow(self, name, frame):
        if self.manager.getFrame(name) is None:   # subpage doesn't exist
            self.addSubpage(name)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = base64.b64encode(buffer).decode('utf-8')
        self.manager.imshow(name, frame)
    
    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = SubpageApp()
    cap = cv2.VideoCapture(0)
    
    threading.Thread(target=app.run).start()
    
    # Continuously capture frames from the webcam and update subpages
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        app.imshow("frame", frame)
        app.imshow("gray", gray)
