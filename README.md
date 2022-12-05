# ANLY 580 Final Project (Natural Language Processing)

This project seeks to investigate and gain insights into political election races and results as found through social media data. Natural language processes are used to explore this topic.

**Case Study:**
- The case study of interest for this project is the 2022 Gubernatorial election in Georgia. 
- The candidates are Stacey Abrams (D) and Brian Kemp (R, Incumbent).

**Steps for Analysis:**
1. Tweets are collected based on a series of search terms regarding the candidates and the election as a whole. 
2. Tweet text data is cleaned and formatted as needed.
3. Cleaned/formatted tweets are used for analysis: 
    - *Volumetric Analysis*: general investigation and EDA of collected tweets (distributions of counts, time series analysis)
    - *Sentiment Analysis*: model-based approach (3 methods) to understand tweet tones
    - *Topic Modeling Analysis*: model-based approach (3 methods) to understanding topics discussed for tweets about each candidate

**Repository Contents:**
- `Data_Collection/` 
    - code for collecting tweets through the Tweepy API
    - all raw data collected
- `Data_Merged/`
    - code for merging all raw data collected over time
    - resulting cumulative datasets for each topic (Kemp)
- `Analysis_Code/`
    - code for performing text cleaning
    - code for performing all analyses (volumetric, sentiment, topic modeling)
    - cleaned datasets
- `Vizualizations/`
    - all figures created through analysis
- `Project_Proposal.pdf`
    - initial proposal for project
- `Final_Presentation.pdf`
    - pdf version of final powerpoint presentation for project
