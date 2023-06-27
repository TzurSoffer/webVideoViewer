from flask import Flask
import threading
import cv2

class SubpageManager:
    def __init__(self):
        self.frames = {}
    
    def imshow(self, name, frame):
        self.frames[name] = frame
    
    def getFrame(self, name):
        return self.frames.get(name, False)

class SubpageApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.manager = SubpageManager()
        self.setupRoutes()
        self.subpages = ""
        self.homePage = "<h1>Subpages for Names</h1><ul>{}</ul>"
    
    def setupRoutes(self):
        self.app.route('/')(self.index)
        self.app.route('/<name>')(self.subpage)
        self.app.route('/imshow/<name>')(self.imshow)
    
    def addSubpage(self, name):
        self.subpages += f'<li><a href="/{name}">{name}</a></li>'

    def index(self):
        print(self.subpages)
        return(self.homePage.format(self.subpages))
    
    def subpage(self, name):
        frame = self.manager.getFrame(name)
        if frame == None:
            return(f'<h1>No subpage found for {name}</h1>')
        return(frame)
    
    def imshow(self, name, frame):
        if type(self.manager.getFrame(name)) == bool:   #< subpage dosn't exists
            self.addSubpage(name)
            self.setupRoutes()

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        self.manager.imshow(name, frame)
    
    def run(self):
        threading.Thread(target=self.app.run).start()
    


if __name__ == '__main__':
    app = SubpageApp()
    app.run()
    app.imshow("Jhon", "<h1>This is the updated frame!</h1>")
    app.imshow("michel", "gay men")
