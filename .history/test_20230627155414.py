from flask import Flask
import threading
import cv2
import time
import numpy as np

class SubpageManager:
    def __init__(self):
        self.frames = {}
    
    def imshow(self, name, frame):
        self.frames[name] = frame
    
    def getFrame(self, name):
        return self.frames.get(name, -1)

class SubpageApp:
    def __init__(self, htmlTemplate="./index.html", port=5000):
        self.app = Flask(__name__)
        self.manager = SubpageManager()
        self.setupRoutes()
        self.htmlTemplate = htmlTemplate
        self.subpages = ""
        self.homePage = "<h1>Subpages for Names</h1><ul>{}</ul>"
    
    def setupRoutes(self):
        self.app.route('/')(self.index)
        self.app.route('/<name>')(self.subpage)
        self.app.route('/imshow/<name>')(self.imshow)
    
    def _loadTemplate(self):
        with open(self.htmlTemplate, "r") as f:
            return(f.read())
    
    def addSubpage(self, name):
        self.subpages += f'<li><a href="/{name}">{name}</a></li>'

    def index(self):
        return(self.homePage.format(self.subpages))
    
    def subpage(self, name):
        frame = self.manager.getFrame(name)
        if frame == None:
            return(f'<h1>No subpage found for {name}</h1>')
        return(frame)
    
    def imshow(self, name, frame):
        if type(self.manager.getFrame(name)) == int:   #< subpage dosn't exists
            self.addSubpage(name)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        self.manager.imshow(name, frame)
    
    def run(self):
        threading.Thread(target=self.app.run).start()
    


if __name__ == '__main__':
    app = SubpageApp()
    app.run()
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        app.imshow("frame", frame)
        app.imshow("gray", gray)
