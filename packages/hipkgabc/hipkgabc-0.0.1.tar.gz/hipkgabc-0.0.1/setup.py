

from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'FusionX'

# Setting up
setup(
    name="hipkgabc",
    version=VERSION,
    author="FusionX (a)",
    author_email="<bar.bendavid@weiamann.ac.il>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="""
    This is a detailed description of your package.

    :Author: Your Name
    :Email: your.email@example.com

    **Features:**

    - Feature 1
    - Feature 2

    **Usage:**

    ```python
    import your_package
    your_package.do_something()
    ```
    """
,
 
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

