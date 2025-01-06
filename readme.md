# README for Web Viewer

## Introduction
The WebVideoViewer is a Python application that allows you to create subpages with live video streams from a webcam or other source. It uses the Flask framework to handle web requests and displays video frames in real-time.

## Requirements
- Python 3.x
- Numpy
- simplejpeg
- Flask

## Installation
### Method 1: Install via pip
1. This library can be installed with pip via this command: ```pip install webStreamViewer```
<details>
  <summary><h2>Manual Installation</h2></summary>
   <p>1. Clone the repository or download the code files.</p>
   <p>2. Install the required dependencies by running the following command:</p>
   <code>pip install -r requirements.txt</code>
</details>

## Usage

1. Import the necessary modules:
   ```python
   import webStreamViewer
   import cv2
   ```

2. Create an instance of the `VideoStream` class:
   ```python
   app = webStreamViewer.VideoStream()
   ```

3. Start the Flask web server on a specified port (default is 80):
   ```python
   app.run()
   ```

4. Continuously capture frames from the webcam and update subpages:
   ```python
   cap = cv2.VideoCapture(0)
   
   while True:
       _, frame = cap.read()
       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       app.imshow("frame", frame)
       app.imshow("gray", gray)
   ```

5. Access the subpages:
   - The home page lists all the available subpages. Visit the root URL (e.g., `http://localhost:80/`) to see the home page which contains the routes to all the subpages.
   - Each subpage displays a live video stream. Add the subpage name to the root URL (e.g., `http://localhost:80/video1`) to access a specific subpage.

## Customization
You can customize the following aspects of the Flask Subpage App:

- **Templates**: The app uses HTML templates to render the home page and subpages. By default, it looks for the templates in the `templates` folder in the library's location. You can specify custom template paths when creating a `VideoStream` instance:
   ```python
   app = VideoStream(homePageTemplate="home.html", subpageTemplate="subpage.html", templatePath="the/path/to/your/templates/folder")
   ```

- **Port**: The default port for the Flask web server is 80. If you want to use a different port, specify it when creating a `VideoStream` instance:
   ```python
   app = VideoStream(port=5000)
   ```


## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
