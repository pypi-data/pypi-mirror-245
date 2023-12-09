from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='camera_API',
    version='0.1.4',
    packages=['camera_API'],
    package_data={
        'camera_API': ['C:\\Users\\Sivabalan-LP\\Videos\\camera_API_try\\camera_API\\cv2\\*',
                       'C:\\Users\\Sivabalan-LP\\Videos\\camera_API_try\\camera_API\\hidapi-0.13.1.dist-info\\*'],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy==1.24.3', 'prettytable==3.8.0',
        # Add other dependencies as needed
    ],

    author='Sivabalan T',
    author_email='sivabalan.t@e-consystems.com',
    description='Used to accessing the camera.',
    classifiers=['Programming Language :: Python :: 3', ],
)
