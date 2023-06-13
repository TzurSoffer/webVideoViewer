# Video Stream Flask Application

This is a simple Flask application that streams video from your webcam using OpenCV. The application displays the video feed on a web page and updates it in real-time.

## How it Works

The application is built using Python, OpenCV, and Flask. It consists of a `VideoStream` class that sets up a Flask web server and handles video streaming. Here's how it works:

1. The `VideoStream` class initializes the Flask application and sets up the routes for the web server.

2. The `/` route renders an HTML template (`index.html`) which will be displayed in the web browser.

3. The `/videoFeed` route is a special route that returns a response containing the video frames as a multipart response. This allows the video frames to be displayed on the web page in real-time.

4. The `videoUpdater` function is a generator function that continuously yields the video frames as a multipart response.

5. The `imshow` method takes a frame from the webcam capture, encodes it as a JPEG image using OpenCV, and stores it in the `self.frame` variable. This frame will be sent as part of the video feed in the `videoUpdater` function.

6. The `run` method starts the Flask application in a separate thread so that it can run concurrently with the main program.

7. The `pause` method pauses the Flask application, this can be reverted using the unpause method.

8. The `unpause` method unpauses the Flask application if its paused, otherwise is does nothing.

## Simple usage

To use the Video Stream Flask application, follow these steps:

1. Install the required dependencies by running the following command:
```
pip install opencv-python flask
```

2. Create a new Python script and import the necessary libraries:
```
import cv2
import webViewer
```

4. Build the `VideoStream` class and run the application.

```
def checkKeyboardInput(videoStream):
    while True:
        input("press enter to stop ")
        videoStream.pause()
        input("press enter to start ")
        videoStream.unpause()

if __name__ == '__main__':
    cap = cv2.VideoCapture(-1)
    videoStream = VideoStream()

    # Start the keyboard input checking thread
    keyboard_thread = threading.Thread(target=checkKeyboardInput, args=(videoStream,))
    keyboard_thread.start()

    try:
        while True:
            _, frame = cap.read()
            videoStream.imshow(frame)
    except Exception as e:
        print(e)
        sys.exit()
```

5. Save the script and run it using the command:
```
python your_script_name.py
```

6. Open your web browser and go to `http://localhost:5000` or `http://serverIP:5000` to view the video stream from your webcam.

## Customization

You can customize the following aspects of the application:

- **HTML Template**: By default, the application uses an HTML template file named `index.html`. You can modify this template or provide your own by specifying the file path when creating the `VideoStream` object.


Feel free to modify the code and experiment with different functionalities to suit your needs.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and use it according to your needs.

## Acknowledgments

-

 This application was inspired by the Flask video streaming tutorial from the [Official Flask Documentation](https://flask.palletsprojects.com/)
- OpenCV - Open Source Computer Vision Library: [https://opencv.org/](https://opencv.org/)
- Flask - A micro web framework written in Python: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)