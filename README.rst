===============================
mos_parser
===============================

.. image:: https://img.shields.io/travis/oscarlucero15/mosparse.svg
        :target: https://travis-ci.org/oscarlucero15/mosparse

.. image:: https://img.shields.io/pypi/v/mosparse.svg
        :target: https://pypi.python.org/pypi/mosparse


Model Output Statistics are the future predictions of models at various locations. They can be downloaded from the National Weather Service in a text format that is easy for humans to read, but difficult for programs to interpret. This makes it difficult for batch analysis and computation of model bias. To facilitate such analysis we have reformatted model output to a nearly universal file format readable by nearly all data analysis programs and programming languages: CSV files. We developed a python script that does this reformatting and used the script to convert model output files from the years 2000 to 2019. We have analyzed the model output data by comparing it to observed data, retrieved from the Global Historical Climatology Network. We created a python library that allows other users to make this conversion without needing to write their own programs, allowing them to perform their own analysis faster. The library can work on large amounts of data at once.


* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) 

Data
-----
* GFS MOS: https://sats.nws.noaa.gov/~mos/archives/mav.html
* GFS MOS MAV Alphanumeric Message: https://www.nws.noaa.gov/mdl/synop/mavcard.php
* GHCN: ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/

Features
--------

Install
-------

.. code:: bash

 git clone https://github.com/ccny-glasslab/mosparse.git
 cd mosparse
 pip install -ve . 
