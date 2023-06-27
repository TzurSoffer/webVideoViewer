from flask import Flask, render_template
import threading
import cv2
import os
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
        self.currentFolder = os.path.dirname(os.path.abspath(__file__, template_folder=self.currentFolder))
        self.app = Flask(__name__)
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
        frame = self.manager.getFrame(name)
        if frame is None:
            return f'<h1>No subpage found for {name}</h1>'
        return render_template(self.subpageTemplate, videoFeedUrl=frame)
    
    def imshow(self, name, frame):
        if self.manager.getFrame(name) is None:   # subpage doesn't exist
            self.addSubpage(name)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
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
