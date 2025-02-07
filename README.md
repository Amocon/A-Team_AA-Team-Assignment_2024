# [AA] Team Assignment 2024/25 | Team 10: The A-Team

## Introduction

This project analyzes EV charging session data with supplementary weather data to optimize charging hub operations. We cleaned and prepared the dataset, examined temporal patterns and seasonality, developed key performance indicators with an additional interactive KPI-Dashboard, identified site characteristics, and performed clustering to classify archetypical charging sessions. Lastly, we built and compared predictive models, including polynomial regression and neural networks, to forecast utilization.

## Installation & Setup 

1. Install [Python 3.11](https://www.python.org/downloads/release/python-3110/)
2. Install [poetry](https://python-poetry.org) 
3. Check whether poetry was correctly installed and added to your path. 
   Execute "poetry --version" in your terminal to check. 
   Use poetry version >= 1.5.0
4. Download the Poetry virtual environment with the Python libraries defined in the [pyproject.toml](pyproject.toml) file. 
   Navigate into the "A-Team_AA-Team-Assignment_2024" folder and excecute "poetry install". -->

## Order of execution

The Python Notebooks are  located in the `aa_team_assignment` directory and should be executed in the order of their numbering, i.e.:
1. 01_data_preparation.ipynb
2. 02_1_temporal_patterns_and_seasonality.ipynb
3. 02_2_kpis.ipynb
4. 02_3_site_characteristics.ipynb
5. 03_clustering_analysis.ipynb
6. 04_utilization_prediction.ipynb

The additional interactive KPI-Dashboard should be started after the `02_2_kpis.ipynb` notebook, since the resulting data of this notebook is neccessary to run it. The KPI-Dashboard can be executed by the following command in the terminal: `poetry run streamlit run KPI-Dashboard.py`