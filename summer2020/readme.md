# Notebooks from Summer 2020 REU/HIRESS

Most weather forecasts do not come directly from weather models, but are based on Model Output Statistics (MOS).  Weather forecasters often adjust model forecasts based on their expertise with the local terrain and climate. Building on previous work processing this dataset, the aim of this project is to explore if these adjustments follow a predictable pattern. 

1. Read in each file in https://sats.nws.noaa.gov/~mos/archives/avnmav/
2. Download all files from source above. Use a "wget" command.
    2a. wget --recursive --no-parent https://sats.nws.noaa.gov/~mos/archives/avnmav/
3. Write parsed station into database & write errors to log for one file.
4. Do above step for all files.
5. Match up GHCN & MOS variables 
6. Compute the errors in the MOS forecast
7. use exploratory data analysis techniques to identify a common signature for errors, 
8. use k-means clustering to explore which error types are prevalent amongst which types of stations. 
