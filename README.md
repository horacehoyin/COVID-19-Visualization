# COVID-19 Visualization in Python

COVID-19 Visualization is a set of Jupyter Notebooks in Python visualizing COVID-19 data obtained from https://ourworldindata.org.

## General Info

This project aims to visualize the historical trends of the global COVID-19 pandemic on Jupyter Notebook.

The project consists of two parts:
-   Download and transform data from https://ourworldindata.org.
-   Visualize the historical trends of countries or regions around the globe.


## Technologies

- Python 3.8.12
- pandas 1.4.1
- matplotlib 3.5.1
- seaborn 0.11.2


## Installation

Use conda to install the conda environment.

```bash
conda env create --file py38-covid.txt
```
Note: The project was developed in Apple Silicon environment.


## Files

There are four main files:

-   ```juh_data.ipynb``` has the below functions:
    -	Download the data provided by https://ourworldindata.org.
    -	Transform the data for use.
    -	Save the downloaded and transformed data as CSVs.

-   ```visualizations.py``` builds functions for visualizations. Visualization includes:
    -	Show the data of a selected country/region.
    -	Show the data of a list of selected countries/regions.
    -	Show the top countries/regions have the highest total number of cases in all time.
    -	Show the top countries/regions have the highest average number of cases in a selected period.

-   ```visualization_notebook.ipynb``` provides examples of how to use the visualization methods.

-   ```visualization_explained.ipynb``` combines ```visualizations.py``` and ```visualization_notebook.ipynb``` with explanations on the methods.


## Usage

1.	Run ```juh-data.ipynb``` to download the dataset.
2.	Run ```visualization_notebook.ipynb``` for visualization.
	-	Change the parameters for different charts.


## Further Development

-	Include more charts of visualization


## Data Source

The data is obtained from https://ourworldindata.org.

Refer to https://github.com/owid/covid-19-data/tree/master/public/data for detailed explaination of the dataset.

Reference:
-   Hannah Ritchie, Edouard Mathieu, Lucas Rodés-Guirao, Cameron Appel, Charlie Giattino, Esteban Ortiz-Ospina, Joe Hasell, Bobbie Macdonald, Diana Beltekian and Max Roser (2020) - "Coronavirus Pandemic (COVID-19)". Published online at OurWorldInData.org. Retrieved from: 'https://ourworldindata.org/coronavirus' [Online Resource]