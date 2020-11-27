#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials as cred
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# In[2]:


#getting the matches info
matches_url='https://cricketapi.platform.iplt20.com//fixtures?tournamentIds=18790&pageSize=100'
mt_req=requests.get(matches_url)
mt_json=mt_req.json()
columns=['series', 'mt_no', 'mt_id', 'mt_dt', 'mt_team1', 'mt_team2', 'mt_venue', 'mt_result',
         'mt_city', 'mt_country', 'mt_highlights', 
         'mt_report', 'mt_team1_abb', 'mt_team1_id', 'mt_team2_abb', 'mt_team2_id']
df_mt=pd.DataFrame(columns=columns)

for i in range(len(mt_json['content'])):        
    #getting the required attributes
    series=mt_json['content'][i]['tournamentLabel']
    mt_no=mt_json['content'][i]['label']
    mt_id=mt_json['content'][i]['scheduleEntry']['matchId']['id']
    mt_dt=mt_json['content'][i]['scheduleEntry']['matchDate']
    try:
        mt_highlights=mt_json['content'][i]['scheduleEntry']['highlightsLink']
    except:
        mt_highlights=''
    try:
        mt_report=mt_json['content'][i]['scheduleEntry']['reportLink']
    except:
        mt_report=''
    mt_venue=mt_json['content'][i]['scheduleEntry']['venue']['fullName']
    mt_city=mt_json['content'][i]['scheduleEntry']['venue']['city']
    mt_country=mt_json['content'][i]['scheduleEntry']['venue']['country']
    try:
        mt_result=mt_json['content'][i]['scheduleEntry']['matchStatus']['text']
    except:
        mt_result=''
    mt_team1=mt_json['content'][i]['scheduleEntry']['team1']['team']['fullName']
    mt_team1_abb=mt_json['content'][i]['scheduleEntry']['team1']['team']['abbreviation']
    mt_team1_id=mt_json['content'][i]['scheduleEntry']['team1']['team']['id']
    mt_team2=mt_json['content'][i]['scheduleEntry']['team2']['team']['fullName']
    mt_team2_abb=mt_json['content'][i]['scheduleEntry']['team2']['team']['abbreviation']
    mt_team2_id=mt_json['content'][i]['scheduleEntry']['team2']['team']['id']    
    
    #creating an array
    arr=[series, mt_no, mt_id, mt_dt, mt_team1, mt_team2, mt_venue, mt_result, mt_city, mt_country, mt_highlights, 
         mt_report, mt_team1_abb, mt_team1_id, mt_team2_abb, mt_team2_id]
    #creating a dataframe
    df_mt_temp=pd.DataFrame([arr], columns=columns)
    #appending the above dataframe into the base dataframe
    df_mt=df_mt.append(df_mt_temp, ignore_index=True)


# In[4]:


## creating a function that gets the score for the match
def match_scorecard(match_id):
    score_url='https://cricketapi.platform.iplt20.com//fixtures/' + str(match_id) +'/scoring'
    score_req=requests.get(score_url)
    score_json=score_req.json()

    #getting the player list for the game (first table)
    match=score_json['matchInfo']['description']
    stadium=score_json['matchInfo']['venue']['fullName']
    city=score_json['matchInfo']['venue']['city']
    team1=score_json['matchInfo']['teams'][0]['team']['abbreviation']
    team2=score_json['matchInfo']['teams'][1]['team']['abbreviation']
    teams=team1 + ' vs ' + team2
    columns=['match', 'match_id', 'stadium', 'city', 'teams', 'player_id', 'player_name']
    df_pl=pd.DataFrame(columns=columns)
    for i in range(2):
        for j in range(11):
            player_id=score_json['matchInfo']['teams'][i]['players'][j]['id']
            player_name=score_json['matchInfo']['teams'][i]['players'][j]['fullName']
            df_pl_temp=pd.DataFrame([[match, match_id, stadium, city, teams, player_id, player_name]], columns=columns)
            df_pl=df_pl.append(df_pl_temp, ignore_index=True)

    ## second table which contains batting stats 
    ##and third table which has bowling stats
    columns_bat=['innings_bat', 'player_id', 'runs', 'balls', 'sr', 'fours', 'sixes']
    columns_bowl=['innings_bowl', 'player_id', 'overs', 'bowl_runs', 'wkts', 'dots', 'maiden', 'eco']
    df_bat=pd.DataFrame(columns=columns_bat)
    df_bowl=pd.DataFrame(columns=columns_bowl)
    for i in range(2):
        innings=score_json['innings'][i]['inningsNumber']

        #battings stats
        for j in range(len(score_json['innings'][i]['scorecard']['battingStats'])):
            player_id=score_json['innings'][i]['scorecard']['battingStats'][j]['playerId']
            runs=score_json['innings'][i]['scorecard']['battingStats'][j]['r']
            balls=score_json['innings'][i]['scorecard']['battingStats'][j]['b']
            try:
                sr=score_json['innings'][i]['scorecard']['battingStats'][j]['sr']
            except:
                sr=''
            fours=score_json['innings'][i]['scorecard']['battingStats'][j]['4s']
            sixes=score_json['innings'][i]['scorecard']['battingStats'][j]['6s']
            arr_bat=[innings, player_id, runs, balls, sr, fours, sixes]
            df_temp_bat=pd.DataFrame([arr_bat],columns=columns_bat)
            df_bat=df_bat.append(df_temp_bat, ignore_index=True)

        #bowling_stats
        for j in range(len(score_json['innings'][i]['scorecard']['bowlingStats'])):
            player_id=score_json['innings'][i]['scorecard']['bowlingStats'][j]['playerId']
            overs=score_json['innings'][i]['scorecard']['bowlingStats'][j]['ov']
            runs=score_json['innings'][i]['scorecard']['bowlingStats'][j]['r']
            wkts=score_json['innings'][i]['scorecard']['bowlingStats'][j]['w']
            dots=score_json['innings'][i]['scorecard']['bowlingStats'][j]['d']
            maiden=score_json['innings'][i]['scorecard']['bowlingStats'][j]['maid']
            eco=score_json['innings'][i]['scorecard']['bowlingStats'][j]['e']    
            arr_bowl=[innings, player_id, overs, runs, wkts, dots, maiden, eco]
            df_temp_bowl=pd.DataFrame([arr_bowl],columns=columns_bowl)
            df_bowl=df_bowl.append(df_temp_bowl, ignore_index=True)

    ##merging the three tables
    global df_dream11
    df_pl_bat=pd.merge(df_pl, df_bat, how='left', on=['player_id'])
    df_pl_bat_bowl=pd.merge(df_pl_bat, df_bowl, how='left', on=['player_id'])
    df_pl_bat_bowl=pd.merge(df_pl_bat_bowl, df_dream11[['player_id', 'role', 'team']], how='left', on=['player_id'])
    
    global ws, lst_row, sheet
    ws_data=ws.get_all_values()
    lst_row=len(ws_data)+1

    df_pl_bat_bowl=df_pl_bat_bowl.fillna('')
    data=df_pl_bat_bowl.values.tolist()
    ws.update('A'+str(lst_row),data)
    
    
    ##input into the excel file by deduping the entries
    #df_exist=pd.read_csv('scorecard.csv')
    #df_exist=df_exist.append(df_pl_bat_bowl, ignore_index=True)
    #df_exist.drop_duplicates(subset=['match_id', 'player_id'], keep='first', ignore_index=True).to_csv('scorecard.csv', index=False)
    #df_pl_bat_bowl.to_csv('scorecard.csv', mode='a')


# In[3]:


#connecting to google sheet
#define the scope
scope=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#add credentials to the account
creds=cred.from_json_keyfile_name('<your json key file name>', scope)

#authorize the client sheet
client=gspread.authorize(creds)

#getting an instance of the spreadsheet
sheet=client.open('<google sheet name>')

#getting the data from the worksheet
ws=sheet.get_worksheet(0)
ws_data=ws.get_all_values()
if len(ws_data)>1:
    df_exist=pd.DataFrame(data=ws_data[1:], columns=ws_data[0])
else:
    df_exist=pd.DataFrame(columns=ws_data[0])

#getting last row
lst_row=len(df_exist)+1


# In[24]:


#finding out the matches not in the scorecard
played_mt=list(df_mt[df_mt['mt_result']!='']['mt_id'])
exist_mt=list(df_exist['match_id'].unique())
exist_mt=[int(m) for m in exist_mt]
missed_mt=list(set(played_mt)-set(exist_mt))

#reading the dream11 list
df_dream11=pd.read_csv('dream11_players.csv')


# In[ ]:





# In[ ]:


#calling the function for the missed matches
for i in missed_mt:
    match_scorecard(i)


# In[ ]:


##automating the tableau refresh notebook
driver=webdriver.Chrome()
driver.get('https://public.tableau.com/s/')
driver.implicitly_wait(5)
driver.find_element_by_class_name('login-link').click()
driver.find_element_by_name("login-email").clear()
driver.find_element_by_name("login-email").send_keys('<your tableau public email id>')
driver.find_element_by_name("login-password").clear()
driver.find_element_by_name("login-password").send_keys('<your password>')
driver.find_element_by_id('signin-submit').click()
driver.implicitly_wait(20)
driver.find_element_by_partial_link_text('<name of your IPL dashboard>').click()
driver.implicitly_wait(20)
driver.find_element_by_class_name('viz-refresh-extract').click()
driver.close()


# In[ ]:





# In[ ]:





# In[ ]:




