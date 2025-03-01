# Machine Learning Project: [Visualization-of-Anomalies-during-Continuous-Casting]

## Overview
This project aims to visualize anomalies in the continuous casting process by mapping temperature values to a color range on a 2D plane. It utilizes PyQt5 to create a graphical user interface (GUI) that displays both the temperature and temperature profile of the mold copper plate. The primary objective is to highlight abnormal heat transfer between molten steel and the mold copper plate during events such as sticking breakouts or longitudinal cracks, where distinct temperature profile patterns emerge.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Models](#models)
- [Results](#results)


## Installation
### Prerequisites
Before running the project, make sure you have the following dependencies installed:

- Python 3.6
- Pip / Conda (Python package manager)
- Necessary Python packages including Pyqt5


## Usage
Running the Model
To run the model, follow these steps:
1. Download all files from this repository and ensure they are placed within the same root directory.
2. Open a terminal, navigate to the directory containing these files, and execute the script by running: python MainWindowShow.py
3. Once the script is executed, a graphical user interface (GUI) will appear, incorporating multiple functions within the panel.
4. Note: We apologize for not including the original dataset, as it is too large and restricted to private use only.

## Project Structure
│  AbnormalAreaDetect.py
│  Add_New_Feature.py
│  BreakoutImagesOutput.py
│  Breakout_List.txt
│  LFC_List.txt
│  MainWindow.py
│  MainWindow.ui
│  MainWindowShow.py
|  README.md
│  Show_Tem_Difference_Thermography.py
│  Show_Thermography.py
│  Tem_TemV_Cal.py
│  __init__.py

## Results
The following is the comparison between normal condition and abnormal condition:
![2015 07 16  07 09 54  内弧宽面Tv](https://github.com/user-attachments/assets/fb025170-f2a3-4219-9754-f2e814772174)

