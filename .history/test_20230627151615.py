from flask import Flask
import threading

class SubpageManager:
    def __init__(self):
        self.frames = {
            'John': '<h1>Welcome to John\'s Subpage!</h1>',
            'Alice': '<h1>Welcome to Alice\'s Subpage!</h1>',
            'Bob': '<h1>Welcome to Bob\'s Subpage!</h1>'
        }
    
    def imshow(self, name, new_frame):
        self.frames[name] = new_frame
    
    def get_frame(self, name):
        return self.frames.get(name)


class SubpageApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.manager = SubpageManager()
        self.setupRoutes()
        self.subpages = ""
    
    def setupRoutes(self):
        self.app.route('/')(self.index)
        self.app.route('/<name>')(self.subpage)
        self.app.route('/imshow/<name>')(self.imshow)
    
    def index(self):
        subpages = ''.join(f'<li><a href="/{name}">{name}</a></li>' for name in self.names)
        return f'<h1>Subpages for Names</h1><ul>{subpages}</ul>'
    
    def subpage(self, name):
        frame = self.manager.get_frame(name)
        if frame is None:
            return f'<h1>No subpage found for {name}</h1>'
        return frame
    
    def imshow(self, name, frame):
        self.manager.imshow(name, frame)
    
    def run(self):
        threading.Thread(target=self.app.run).start()
    


if __name__ == '__main__':
    app = SubpageApp()
    app.run()
    app.imshow("Jhon", "<h1>This is the updated frame!</h1>")
