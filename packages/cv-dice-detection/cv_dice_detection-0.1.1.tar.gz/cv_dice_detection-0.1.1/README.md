# Dice Detection

A Computer Vision project. [Documentation Link](https://vigrel.github.io/dice-detection/)

Developed by: 
- Arthur Chieppe
- Luiza Valezim
- Vinícius Eller

An API developed with the goal to use Computer Vision and Machine Learning in order to identify and sum the values of the total dices.

## Using the repository 

1. Clone the repo
   ```sh
    git clone https://github.com/Vigrel/dice-detection.git
   ```
2. Create and activate virtualenv
   ```sh
    cd dice-detection/
    python3 -m virtualenv .venv
    source .venv/bin/activate
   ```
3. Run a demo
   ```sh
   python3 src/dice_detection_demo.py
   ```

## Configuring the Environment

To ensure dice detection accuracy, set up the environment as follows:

1. **Surface**: Place a white piece of paper on the table for dice rolling. The white background enhances contrast for better detection.

2. **Camera Position**: Position the camera in a top-down view, parallel to the table surface. The camera height should be 40 centimeters above the table for a clear and consistent perspective.

3. **Adjust CAMERA_DISTANCE**: In the configuration module, adjust the `CAMERA_DISTANCE` parameter to reflect the actual distance in centimeters between the camera and the table surface. This parameter is crucial for accurate calculations and reliable dice number detection.

4. **Camera Calibration (if necessary)**: Calibrate the camera if needed for accurate measurements. Refer to your camera documentation for calibration procedures.

Follow these guidelines to create an environment for effective dice detection, ensuring optimal system performance.