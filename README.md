# DSCI-532_2025_13_tbd
DSCI 532 Dashboard Projects

# Project Summary 

Moving to a new country presents many challenges. One key factor that new immigrants must consider is safety. The USA Crime Tracker Dashboard is an interactive Shiny application that enables users to explore historical crime trends across the United States of America. Through coordinated visualizations and summary metrics, the app helps users identify geographic patterns, temporal trends, and relative crime risk to empower immigrants in making informed decisions about their safety when moving to the USA.

Link to Published Stable Dashboard: <https://connect.posit.cloud/dvorster/content/019ca5bd-b008-a68f-3889-89a1f04e0011>
Link to Published Preview Dashboard: <https://connect.posit.cloud/dvorster/content/019ca5be-a481-ae37-df72-5e656d070507>

# Running the App Locally 

## 1. Close the Repository 

```bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_13_usa-crime-tracker.git
cd DSCI-532_2026_13_usa-crime-tracker
```

## 2. Create the Conda Environment 

```bash
conda env create -f environment.yml
conda activate usa-crime-tracker
```

## 3. Run the Shiny App 

```bash
shiny run src/app.py
```

Open your web browser and navigate to the url below:

<http://127.0.0.1:8000>


## 4.Stop the App
In the terminal, enter: 
```bash
Ctrl + C
```

