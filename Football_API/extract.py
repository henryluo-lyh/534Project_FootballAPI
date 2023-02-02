import pandas as pd
import requests
import json
import urllib.parse
import time
from pandas import json_normalize
from MyThread import MyThread
import os
from multiprocessing import Pool


headers = {
    'X-RapidAPI-Key': 'e5cd8b6e5amsh39bfb2d72f1af22p19c842jsn8935c4a31ddb',
    'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
    }



def json2dict(str_text):
    return json.loads(str_text)



def build_query(base_url, endpoint, params = {}):
    
    return base_url + endpoint + ('?' if params else '') + urllib.parse.urlencode(params)



def call_api(base_url, endpoint, params = {}):
    
    # build url
    url = build_query(base_url, endpoint, params)

    response = requests.request("GET", url, headers=headers)
    
    return response



# def get_players_json_data(league, season, page = 1, players_json_data = []):
    
#     base_url = "https://api-football-v1.p.rapidapi.com/v3/"
#     response = call_api(base_url, 'players', {'league':league, 'season':season, 'page':page})
    
#     one_page_players_dict = json2dict(response.text)
#     players_json_data.append(one_page_players_dict)
    
#     print('League: {}, Season: {}'.format(league, season))
#     print(one_page_players_dict['paging']['current'], one_page_players_dict['paging']['total'])
    
#     if(one_page_players_dict['paging']['current'] < one_page_players_dict['paging']['total']):
        
#         page = page + 1
        
#         # time.sleep(0.1) # 根据pricing调整
        
#         get_players_json_data(league, season, page, players_json_data)
        
#     return players_json_data



def get_players_json_data(league, season, page = 1, players_json_data = []):
    
    base_url = "https://api-football-v1.p.rapidapi.com/v3/"
    response = call_api(base_url, 'players', {'league':league, 'season':season, 'page':page})
    
    one_page_players_dict = json2dict(response.text)
    players_json_data.append(one_page_players_dict)
    
    print('League: {}, Season: {}'.format(league, season))
    print(one_page_players_dict.get('paging').get('current'), 
          one_page_players_dict.get('paging').get('total'))
    
    if(one_page_players_dict.get('paging').get('current') < one_page_players_dict.get('paging').get('total')):
        
        page = page + 1
        
        # time.sleep(1) # 根据pricing调整
        
        get_players_json_data(league, season, page, players_json_data)
        
    return players_json_data



def get_players_df_data(league, season):
    
    players_json_data = get_players_json_data(league, season)
    
    reponse_df = json_normalize(players_json_data, 
                        record_path=['response'])

    statistics_df = json_normalize(players_json_data,
                        record_path=['response', 'statistics'], meta = [['response', 'player', 'id']])

    players_df_data = pd.merge(statistics_df, reponse_df, left_on='response.player.id', right_on='player.id')

    players_df_data.drop(['response.player.id', 'statistics'], axis=1, inplace=True)
    
    return players_df_data



def df2csv_perSeasonLeague(df):
    df.to_csv(f"{df['league.name'][0]}-{df['league.season'][0]}-players.csv", encoding='utf_8_sig')
    
    
    
def df2csv_total(df):
    if not os.path.exists('total-players.csv'):
        df.to_csv('total-players.csv',encoding='utf_8_sig',mode='a',index=False,index_label=False)
    else:
        df.to_csv('total-players.csv', encoding='utf_8_sig', mode='a', index=False, index_label=False,header=False)

def get_2_players_data(league1, season1, league2, season2):
    
    try:
        records = pd.read_csv('input_record.csv')
    except Exception as ex:
        print(ex)
    
    ths = []
    if league1 == league2 and season1 == season2:
        if records[ (records.league == league1) & (records.season == season1) ].empty:
            input_record2csv(league1, season1)
            df1 = get_players_df_data(league1, season1)
    else:
        if records[ (records.league == league1) & (records.season == season1)].empty:
            input_record2csv(league1, season1)
            df1 = get_players_df_data(league1, season1)
        
        if records[ (records.league == league2) & (records.season == season2) ].empty:
            input_record2csv(league2, season2)
            df2 = get_players_df_data(league2, season2)
    
    
    print('search done')
    
    t = pd.concat([df1, df2], axis = 0)
    
    df2csv_total(t)

    return t

def get_2_players_data_multithread(league1, season1, league2, season2):
    
    try:
        records = pd.read_csv('input_record.csv')
    except Exception as ex:
        print(ex)
    
    ths = []
    if league1 == league2 and season1 == season2:
        if records[ (records.league == league1) & (records.season == season1) ].empty:
            th1 = MyThread(get_players_df_data, (league1, season1))
            ths.append(th1)
            input_record2csv(league1, season1)
    else:
        if records[ (records.league == league1) & (records.season == season1)].empty:
            th1 = MyThread(get_players_df_data, (league1, season1))
            ths.append(th1)
            input_record2csv(league1, season1)
        
        if records[ (records.league == league2) & (records.season == season2) ].empty:
            th2 = MyThread(get_players_df_data, (league2, season2))
            ths.append(th2)
            input_record2csv(league2, season2)

    print(len(ths))   
     
    for th in ths:
        th.start()
        
    for th in ths:
        th.join()
    
    
    print('search done')
    
    t = pd.DataFrame()
    for th in ths:
        print(1)
        t = pd.concat([t, th.get_result()], axis = 0)
    
    df2csv_total(t)

    return t



def input_record2csv(league, season):
    
    dict = {
        'league': [league],
        'season': [season]
    }
    
    df = pd.DataFrame(dict)
    
    if not os.path.exists('input_record.csv'):
        df.to_csv('input_record.csv',encoding='utf_8_sig',mode='a',index=False,index_label=False)
    else:
        df.to_csv('input_record.csv', encoding='utf_8_sig', mode='a', index=False, index_label=False,header=False)

    # pd.DataFrame(dict).to_csv(r"input_record.csv", mode = 'a')




    




    

