import pandas as pd

# drop the player.photo column to avoid duplicates which only differ in the photo's url link
def trim_df(df):
    df = df.drop(columns = ["player.photo", "team.logo", "league.logo", "league.flag"])
    df = df.drop_duplicates()
    return df

# search player from df by name and season
def search(df):
    df = trim_df(df)
    name = input('name: ').capitalize()
    year = int(input("Season: "))

    rs =df[(df['player.name'].str.contains(f'.*{name}.*')) & (df['league.season'] == year)] 

    return rs

# search for two players to compare, return player stats in a single dataframe,
# prompt user to specify player id if initial search yeilded more than one player,
# prompt user to re-enter player name if search() returns no result
def search_players(df):
    results = ['','']

    for i in range(2):
        results[i] = search(df)
        while len(results[i]) <1:
            print("player not found, please try again")
            results[i] = search(df)
        if len(results[i]) >1:
            print(results[i][ ['player.name', 'player.id' ]])

            player_id = int(input('specify player id: '))
            results[i] = results[i][ results[i]['player.id'] == player_id ]
        print("registered: {}".format(results[i]["player.name"].tolist()))
    return pd.concat(results)
    
# retain specific sets of stats according to player's position, pivote dataframe longer
# to facilitate visualization, concat player.name and league.season to distinguish same player
# from different years
def process_df(rs_df):
    positions = []

    for index, row in rs_df.iterrows():
        positions.append(row['games.position'])
    if positions[0] == positions[1]:
        if positions[0] == 'Attacker':
            rs_df = rs_df[['player.lastname','league.season','games.lineups', 'games.appearences', 'games.rating','goals.total', 'fouls.committed',
                    'goals.assists', 'shots.on']]
        elif positions[0] == 'Defender':
            rs_df = rs_df[['player.lastname','league.season','games.lineups', 'games.appearences',  'games.rating','goals.total', 'fouls.committed',
                'goals.assists', 'tackles.total']]
        elif positions[0] == 'Midfielder':
            rs_df = rs_df[['player.lastname','league.season','games.lineups', 'games.appearences',  'games.rating','goals.total','fouls.committed',
                'goals.assists', 'passes.key']]
        elif positions[0] == 'Goalkeeper':
            rs_df = rs_df[['player.lastname','league.season','games.lineups', 'games.appearences', 'games.rating','penalty.saved','fouls.committed',
                'goals.conceded', 'goals.saves']]
    else: 
        rs_df = rs_df[['player.lastname','league.season','games.lineups', 'games.appearences', 'games.rating','goals.total','fouls.committed',
                   'goals.assists']]
    pd.options.mode.chained_assignment = None
    rs_df.loc[:,"player.lastname"] = rs_df.loc[:,'player.lastname'] +" "+ rs_df.loc[:,"league.season"].astype(str)
    rs_df = rs_df.drop(columns = ["league.season"])
    

    rs_df = rs_df.melt(id_vars=["player.lastname"], 
            var_name="stats", 
            value_name="value")
    rs_df = rs_df.sort_values(by=['stats'])


    return rs_df
