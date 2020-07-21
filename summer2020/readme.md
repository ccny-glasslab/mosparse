# Notebooks from Summer 2020 REU/HIRESS

Most weather forecasts do not come directly from weather models, but are based on Model Output Statistics (MOS).  Weather forecasters often adjust model forecasts based on their expertise with the local terrain and climate. Building on previous work processing this dataset, the aim of this project is to explore if these adjustments follow a predictable pattern. 

0. read in each file in https://sats.nws.noaa.gov/~mos/archives/avnmav/
2. write parsed station into database & write errors to log
    1. to prepare for this step, write out all the stations in 1 mav file to csvs/logs (1 csv/log per station)
4. match up GHCN & MOS variables 
1. compute the errors in the MOS forecast
2. use exploratory data analysis techniques to identify a common signature for errors, 
3. use k-means clustering to explore which error types are prevalent amongst which types of stations. 
