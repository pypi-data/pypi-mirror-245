from setuptools import setup, find_packages

setup(
    name='camera_API',
    version='0.0.3',
    packages=['camera_API'],
    install_requires=[
        'opencv-python==4.5.5.62', 'hidapi==0.13.1', 'numpy==1.24.3', 'prettytable==3.8.0',
        # Add other dependencies as needed
    ],

    author='Sivabalan T',
    author_email='sivabalan.t@e-consystems.com',
    description='Used to accessing the camera in friendly way',
    classifiers=['Programming Language :: Python :: 3',],
)