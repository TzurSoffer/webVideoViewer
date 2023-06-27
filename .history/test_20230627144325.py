from flask import Flask, render_template

app = Flask(__name__)

class VideoPlayer:
    def imshow(self, name, frame):
        @app.route('/video/<name>/')
        def video_page(name):
            return render_template('video.html', name=name, frame=frame)

        app.run()

# Example usage
player = VideoPlayer()
player.imshow('example_video', 'example_frame')
