from flask import Flask

app = Flask(__name__)

# Dictionary to store the frames for each name
frames = {
    'John': '<h1>Welcome to John\'s Subpage!</h1>',
    'Alice': '<h1>Welcome to Alice\'s Subpage!</h1>',
    'Bob': '<h1>Welcome to Bob\'s Subpage!</h1>'
}

@app.route('/')
def index():
    names = ['John', 'Alice', 'Bob']  # Replace with your list of names
    subpages = ''.join(f'<li><a href="/{name}">{name}</a></li>' for name in names)
    return f'<h1>Subpages for Names</h1><ul>{subpages}</ul>'

@app.route('/<name>')
def subpage(name):
    frame = frames.get(name)
    if frame is None:
        return f'<h1>No subpage found for {name}</h1>'
    return frame

@app.route('/update/<name>')
def update(name):
    new_frame = '<h1>This is the updated frame!</h1>'
    frames[name] = new_frame
    return f'Frame for {name} has been updated.'

if __name__ == '__main__':
    app.run()
