# Automated ETL Tableau Dashboard

Indian Premier League (or IPL) is cricket tournament played in a franchise format. I built this dashboard to keep track of the performances of each team and players in each match. Moreover it was an effort to utilize the skills of web scraping and creating Tableau dashboard into a self sustained ETL pipeline.

You can check the dashboard [here](https://public.tableau.com/profile/chandrish.avm#!/vizhome/IPL2020_16023965309280/Dashboard1).

The pipeline consists of the following steps:
1. Collect the scores and related stats of matches by web scraping of the IPL website
2. Using Google API, put the data into a google sheet which is linked to my Tableau Public Dashboard
3. Log in to my Tableau Public profile and click "Refresh Update" button using a selenium web driver

The dashboard was refreshed using [ipl_2020.py](https://github.com/avmchandrish/ipl-2020-tracker/blob/master/ipl_2020.py) everyday.
This was achieved by scheduling this python script in my Windows scheduler at a particular time.
