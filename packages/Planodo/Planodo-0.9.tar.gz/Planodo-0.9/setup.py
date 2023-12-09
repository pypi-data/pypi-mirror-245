from distutils.core import setup

setup(
    name="Planodo",
    version="0.9",
    description="Utility library for creating large zoomable images",
    author="Etienne Posthumus",
    author_email="ep@epoz.org",
    url="https://github.com/epoz/planodo",
    py_modules=["planodo"],
    install_requires=["progress"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
