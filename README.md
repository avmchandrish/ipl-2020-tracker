# ipl-2020-tracker
A python script which creates the data pipeline for refreshing my tableau dashboard everyday.  

Indian Premier League or IPL is in general a long cricket tournament spanning around two to three months.
Being an ardent cricket fan myself, it becomes difficult to keep track of the performances of each team and players in each match.

I made a basic tableau dashboard which gives me performance of players by team for all the matches they featured in. 
You can check this out at:
https://public.tableau.com/profile/chandrish.avm#!/vizhome/IPL2020_16023965309280/Dashboard1

This dashboard had to be refreshed everyday, so this python script was scheduled to run in my windows scheduler at a particular time.
The code does the following:
1. Gets the scores and performances of players from IPL T20 site (for the missing matches in the database)
2. Pushes this data into a google sheet which is linked to my Tableau Public Dashboard
3. Logs in to my Tableau Public profile and clicks "Refresh Update" button using a selenium web driver


