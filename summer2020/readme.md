# Notebooks from Summer 2020 REU/HIRESS

Most weather forecasts do not come directly from weather models, but are based on Model Output Statistics (MOS).  Weather forecasters often adjust model forecasts based on their expertise with the local terrain and climate. Building on previous work processing this dataset, the aim of this project is to explore if these adjustments follow a predictable pattern. 

1. Read in each file in https://sats.nws.noaa.gov/~mos/archives/avnmav/
2. Download all files in format above. "wget" command.
2. Write parsed station into database & write errors to log.

3. Match up GHCN & MOS variables 
4. compute the errors in the MOS forecast
5. use exploratory data analysis techniques to identify a common signature for errors, 
6. use k-means clustering to explore which error types are prevalent amongst which types of stations. 
