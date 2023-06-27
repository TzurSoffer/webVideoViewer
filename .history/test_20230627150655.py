from flask import Flask

app = Flask(__name__)

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

manager = SubpageManager()

@app.route('/')
def index():
    names = ['John', 'Alice', 'Bob']  # Replace with your list of names
    subpages = ''.join(f'<li><a href="/{name}">{name}</a></li>' for name in names)
    return f'<h1>Subpages for Names</h1><ul>{subpages}</ul>'

@app.route('/<name>')
def subpage(name):
    frame = manager.get_frame(name)
    if frame is None:
        return f'<h1>No subpage found for {name}</h1>'
    return frame

@app.route('/update/<name>')
def update(name):
    new_frame = '<h1>This is the updated frame!</h1>'
    manager.imshow(name, new_frame)
    return f'Frame for {name} has been updated.'

if __name__ == '__main__':
    import threading
    threading.Thread(target=app.run).start()
    manager.imshow("John", "test")
