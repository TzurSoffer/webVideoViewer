from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    names = ['John', 'Alice', 'Bob']  # Replace with your list of names
    subpages = ''.join(f'<li><a href="/{name}">{name}</a></li>' for name in names)
    return f'<h1>Subpages for Names</h1><ul>{subpages}</ul>'

@app.route('/<name>')
def subpage(name):
    frame_content = f'<h1>Welcome to {name}\'s Subpage!</h1>'
    frame = f'<iframe srcdoc="{frame_content}" style="width:100%; height:100%; border:none;"></iframe>'
    return frame

if __name__ == '__main__':
    app.run()
