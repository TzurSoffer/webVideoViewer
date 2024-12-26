from setuptools import setup, find_packages

setup(
    name="webStreamViewer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "simplejpeg",
        "flask",
    ],
    package_data={
        'webStreamViewer': ['templates/*.html']
    },
    author="Tzur Soffer",
    author_email="tzur.soffer@gmail.com",
    description="opencv-style image display that displays the image/stream on a local webserver instead of a screen.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TzurSoffer/webVideoViewer/tree/main",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
