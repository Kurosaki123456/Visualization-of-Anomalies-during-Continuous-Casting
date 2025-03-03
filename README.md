# [Visualization-of-Anomalies-during-Continuous-Casting]

## Overview
This project aims to visualize anomalies in the continuous casting process by mapping temperature values to a color range on a 2D plane. It utilizes PyQt5 to create a graphical user interface (GUI) that displays both the temperature and temperature profile of the mold copper plate. The primary objective is to highlight abnormal heat transfer between molten steel and the mold copper plate during events such as sticking breakouts or longitudinal cracks, where distinct temperature profile patterns emerge.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Results](#results)


## Installation
### Prerequisites
Before running the project, make sure you have the following dependencies installed:

- Python: version 3.6 or higher.
- Pip / Conda (Python package manager)
- Required Python package including Pyqt5.


## Usage
### Running the Model
To run the model, follow these steps:
1. Download all files from this repository and ensure they are placed within the same root directory.
2. Open a terminal, navigate to the directory containing these files, and execute the script by running: python MainWindowShow.py
3. Once the script is executed, a graphical user interface (GUI) will appear, incorporating multiple functions within the panel.
4. Note: We apologize for not including the original dataset, as it is too large and restricted to private use only.

## Project Structure
The project is organized as follows:

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

Sticking breakout (with a distinct V-shaped distribution)

![2015 07 16  07 09 54  内弧宽面Tv](https://github.com/user-attachments/assets/fb025170-f2a3-4219-9754-f2e814772174)

Non sticking breakout (norml condition)

![2016 02 08  00 54 14  外弧宽面Tv](https://github.com/user-attachments/assets/5148b24b-76ea-4a42-af3b-2dd94f8e3524)


Longitudinal crack (consisted of a upper red region and lower blued region)

![2017 03 13  14 40 49  第一排  外弧宽面Td  4](https://github.com/user-attachments/assets/fbceab72-7bf8-4d3e-b4e2-63145cd1a057)

Non longitudinal crack (normal condition)

![2017 11 29  14 24 10  第二排  外弧宽面Td  24](https://github.com/user-attachments/assets/c9da76c1-df52-457e-86bd-e17f5553d96f)

