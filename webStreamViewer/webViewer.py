from flask import Flask, Response, render_template, request
import threading
import simplejpeg
import numpy as np
import os
import base64

def toJPEG(image, quality=100, colorspace="BGR"):
    if isinstance(image, list):
        image = np.array(image)
    image = image.astype(np.uint8)

    if len(image.shape) == 2:
        colorspace = "GRAY"
        image = np.expand_dims(image, axis=2)
    return(simplejpeg.encode_jpeg(image, quality=quality, colorspace=colorspace))

class SubpageManager(dict):
    def __getitem__(self, __key):
        return(self.get(__key, None))

class VideoStream():
    """
    """
    def __init__(self, homePageTemplate=None, subpageTemplate=None, templateFolder=None, port=80):
        """
        Initializes a VideoStream object.

        Args:
            homePageTemplate (str): Path to the home page template file.
            subpageTemplate (str): Path to the subpage template file.
            port (int): Port number for the Flask application.
        """

        if templateFolder == None:
            templateFolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
            print(f"Using default template folder: {templateFolder}")

        self.app = Flask(__name__, template_folder=templateFolder)
        self.manager = SubpageManager()
        self.port = port

        if homePageTemplate is None:
            homePageTemplate = "home.html"
        if subpageTemplate is None:
            subpageTemplate = "subpage.html"

        self.homePageTemplate = homePageTemplate
        self.subpageTemplate = subpageTemplate

        self.setupRoutes()

    def setupRoutes(self) -> None:
        """Sets up the routes for the Flask application"""
        self.app.route('/')(self.index)  #< Define the route for the home page
        self.app.route('/shutdown', methods=['POST'])(self._shutdownFlask)
        self.app.route('/<name>')(self.renderTemplate)  #< Define the route for the subpages
        self.app.route('/<name>/videoFeed')(self.subpage)  #< Define the route for the video feed of each subpage

    def index(self) -> str:
        """Returns the rendered HTML content for the home page"""
        return(render_template(self.homePageTemplate, subpages=list(self.manager.keys())))  #< Render the home page template

    def renderTemplate(self, name) -> str:
        """Returns the rendered subpage(str)"""
        return(render_template(self.subpageTemplate, video_feed=f"/{name}/videoFeed"))  #< Render the subpage template

    def subpage(self, name):
        """
        Generates imgs for the subpage.

        Args:
            name (str): Name of the subpage.

        Returns:
            Response: Response object containing the generated imgs.
        """
        def generate_imgs():
            while True:
                img = self._getImg(name)
                if img:
                    yield b'--img\r\n'
                    yield b'Content-Type: image/jpeg\r\n\r\n'
                    yield base64.b64decode(img)  #< Return the img in the response
                else:
                    yield b'--img\r\n'
                    yield b'Content-Type: text/html\r\n\r\n'
                    yield b'<h1>No subpage found for {name}</h1>\r\n\r\n'  #< Return a message if no img is found for the subpage

        return Response(generate_imgs(), mimetype='multipart/x-mixed-replace; boundary=img')  #< Return the response object
    
    def _getImg(self, name):
        return(self.manager[name])
    
    def _setImg(self, name, img) -> None:
        self.manager[name] = img

    def imshow(self, name, img) -> None:
        """ Displays an image "img" on the subpage "name" """
        buffer = toJPEG(img)                        #< Encode the img as a JPEG image
        img = base64.b64encode(buffer).decode('utf-8') #< Encode the image data as base64 string
        self._setImg(name, img)                        #< Store the img in the SubpageManager

    def run(self) -> None:
        """Runs the Flask application in a separate thread"""
        threading.Thread(target=self.app.run, kwargs={"host": "0.0.0.0", "port": self.port}).start()  #< Run the Flask application in a separate thread

    def _shutdownFlask(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def stop(self) -> None:
        """Stops the Flask application"""
        with self.app.test_client() as client:
            client.post('/shutdown')     #< simulate a post request to trigger the shutdown signal


if __name__ == '__main__':
    import cv2
    import time

    cap = cv2.VideoCapture(0)  #< Open the webcam capture device
    app = VideoStream()        #< Create a VideoStream object
    app.run()                  #< Run the Flask application

    # Continuously capture imgs from the webcam and update subpages
    while True:
        _, frame = cap.read()                          #< Read a frame from the webcam
        time.sleep(1)
        app.imshow("frame", frame)                     #< Display the frame on the "frame" subpage

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #< Convert the frame to grayscale
        app.imshow("gray", gray)                       #< Display the grayscale frame on the "gray" subpage
