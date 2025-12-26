## Dynamic Skills Finder - Analyst Track

<p align="center">
    <img src="/images/dsf_logo_shortcut_circle.png" width="200" height="200">
</p>

#### Introduction

Dynamic Skills Finder is an end-to-end data project.

It starts with an ELT process where data is first downloaded from Skillcorner’s Opendata GitHub repository, which is then stored and later processed following a “medallion” architecture. It creates a DeltaLake-based datalakehouse. In the “bronze” layer, raw data is stored as it arrives. Next, in the “silver” layer, data is transformed to create fact tables and their corresponding dimension tables in a star schema format. Finally, in the “gold” layer, we define final views and aggregated tables for players and teams, ready for consumption.

The second part of the project is an R Shiny web app that feeds directly from the DeltaLake. Its purpose is to facilitate the search for tactical team patterns or player scouting using Dynamic Event Data. To achieve this, the app includes various filters, charts, and tables that allow users to uncover insights not possible with other types of data. Additionally, each Dynamic Event can be visualized in video.

<br>
<p align="center">
    <img src="/images/tactical_find_tracking.png" width="500" height="250">
</p>
<br>

#### Usecases

This app allows off-ball tactical analysis of teams in multiple ways, thanks to its wide range of filters and controls and its diverse options for visualizing information through multiple charts, tables and video.

You can also perform player scouting and compare players using over 130 aggregated metrics created from Dynamic Event Data.

#### Potential Audience

Dynamic Skills Finder can be used across various departments within a club. Tactical analysts, scouts, and sporting directors can enhance their work with off-ball insights.

---

## Video URL

<a href="https://youtu.be/RDQAqNRKvuE" target="_blank">Dynamic Skills Finder Video</a>

---

## Run Instructions

To run the project locally:

1. Open a python terminal and navigate to ‘etl/src’ folder:

   ```bash
   pip install -r requirements.txt
   python elt.py
   ```

2. Open an R console and navigate to ‘apps/dynamicSkillsFinder’ folder:

   ```bash
   install.packages("renv")
   renv::restore()
   source("app.R")
   launch_app()
   ```
---

## URL to Web App

To try the app: <a href="https://ob-projects-dynamicskillsfinder.share.connect.posit.cloud/" target="_blank">Dynamic Skills Finder App</a>