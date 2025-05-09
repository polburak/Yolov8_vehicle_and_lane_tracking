# Yolov8_vehicle_and_lane_tracking
This project is a Python-based computer vision application that performs real-time vehicle detection, tracking, lane identification, and incoming/outgoing direction analysis on a predefined video.

## Project Structure ##
    ├── main.py
    ├── modules/
    │   ├── detector.py          
    │   ├── tracker.py           
    │   ├── logger.py            
    │   ├── lane_loader.py       
    ├── lane_selector.py         
    ├── show_lane_test.py        
    ├── lanes/
    │   └── lanes.json           
    ├── input/
    │   └── video1.mp4           
    ├── output/
    │   ├── video1_result.mp4   
    │   └── video1_log.txt       

## Module Overview  ##
| File Name             | Description                                                                                                |
| ----------------------| -----------------------------------------------------------------------------------------------------------|
| `main.py`             | Main script of the project. Performs vehicle detection and tracking, direction analysis, and lane matching.| 
| `detector.py`         | Performs vehicle detection using the YOLOv8 model. Filters only specific vehicle classes.                  |
| `tracker.py`          | Assigns IDs to each vehicle and tracks them using a simple distance-based algorithm.                       |
| `logger.py`           | Logs incoming/outgoing vehicle counts, lane-based transitions, and timestamped events.                     |
| `lane_loader.py`      | Loads predefined lane definitions and detects which lane a point belongs to.                               |
| `lane_selector.py`    | Allows the user to draw lane regions interactively on the video using mouse clicks.                        |
| `show_lane_test.py`   | Used to test and visualize the accuracy of lane regions on a sample frame. 
    

## [Click here to download the test video](https://drive.google.com/file/d/1v5Hh2fll-8pAtMIrMuP1mIsLRkn9lnN-/view?usp=sharing) ## 

## [Click here to download the processed output video](https://drive.google.com/file/d/1V60vCSv-gAfhNB3mM55zURU1JXkbPTVX/view?usp=sharing) ##
