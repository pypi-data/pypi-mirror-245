from setuptools import find_packages, setup

setup(
    name='cv_dice_detection',
    packages=find_packages(),
    version='0.1.1',
    description='An API developed to identify and sum the values of the total dices.',
    long_description="""Welcome to the documentation for our Computer Vision class project.
This Python library has been developed to detect live-streamed dice numbers. 
The objective is to provide a straightforward tool for identifying and analyzing 
dice numbers in real-time. This documentation offers detailed information on 
the library's functionalities, installation procedures, and practical examples 
to facilitate the utilization of our solution. The project is a reflection of our 
exploration into the world of Computer Vision, born out of the requirements
of our class assignment. We invite you to navigate through this documentation as
we delve into the intricacies of dice detection using Python""",
    author='Arthur Chieppe, Luiza Valezim, Vinicius Eller',
    license='MIT',
    zip=False
)
