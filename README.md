# GAnalytics
This is an app for querying Google Analytics data. 

##Prerequisite
  - Python 2.7
    https://www.python.org/downloads/
  - Google Analytics API for Python
    `pip install --upgrade google-api-python-client`

##Usage
  1. Go to working directory in terminal
    `cd ~/...`
  2. Create configuration file (default: setup.txt)
    `python create_config.py <config_file_name>`
  3. Query data
    `python GAnalytics.py --setup <config_file_name>`

##Reference
  - Dimensions & Metrics Explorer:
    https://developers.google.com/analytics/devguides/reporting/core/dimsmets

  - Google Analytics API.data.ga Documentation:
    https://developers.google.com/resources/api-libraries/documentation/analytics/v3/python/latest/analytics_v3.data.ga.html
