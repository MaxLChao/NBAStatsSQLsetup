import os
import pandas as pd
import sys
dir_in = sys.argv[1]
sqldb = '/Users/Max_1/Documents/code/NBAStatsSQLsetup/sqldb'
import sqlalchemy
import mysql.connector
from sqlalchemy import create_engine, text, Table, Column, Integer, String, Float, MetaData
import subprocess

engine = create_engine('mysql+mysqlconnector://root@localhost')

with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS NBAPlayerStats2023_24"))
    conn.execute(text("USE NBAPlayerStats2023_24"))

#update
engine = create_engine('mysql+mysqlconnector://root@localhost/NBAPlayerStats2023_24')
# create our table formats
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
metadata = MetaData()

#player table
players = Table('players', metadata,
                Column('ID', Integer, primary_key=True),
                Column('PLAYER', String(100)),
                Column('TEAM', String(10)),
                Column('AGE', Integer),
                Column('HEIGHT', Float),
                Column('WEIGHT', Integer)
                )
#advanced
advanced = Table('advanced', metadata,
                 Column('ID', Integer, primary_key=True),
                 Column('PLAYER', String(100)),
                 Column('TEAM', String(50)),
                 Column('AGE', Integer),
                 Column('GP', Integer),
                 Column('W', Integer),
                 Column('L', Integer),
                 Column('MIN', Float),
                 Column('OFFRTG', Float),
                 Column('DEFRTG', Float),
                 Column('NETRTG', Float),
                 Column('ASTP', Float), #name='AST%'),
                 Column('AST_TO', Float),
                 Column('AST_RATIO', Float),
                 Column('OREBP', Float), #, name='OREB%'),  # OREB%
                 Column('DREBP', Float), #name='DREB%'),  # DREB%
                 Column('REBP', Float), #name='REB%'),   # REB%
                 Column('TO_RATIO', Float),
                 Column('EFGP', Float), #name='EFG%'),   # EFG%
                 Column('TSP', Float), #name='TS%'),    # TS%
                 Column('USGP', Float), #name='USG%'),   # USG%
                 Column('PACE', Float),
                 Column('PIE', Float),
                 Column('POSS', Integer)
                 )

#defense
defense = Table('defense', metadata,
                Column('ID', Integer, primary_key=True),
                Column('PLAYER', String(100)),
                Column('TEAM', String(50)),
                Column('AGE', Integer),
                Column('GP', Integer),
                Column('W', Integer),
                Column('L', Integer),
                Column('MIN', Float),
                Column('DEF_RTG', Float),
                Column('DREB', Float),
                Column('DREB_PCT', Float), #name='DREB%'),
                Column('DREB_PCT_TEAM', Float), #name='%DREB'),
                Column('STL', Float),
                Column('STL_PCT', Float), #name='STL%'),
                Column('BLK', Float),
                Column('BLK_PCT', Float), #name='%BLK'),
                Column('OPP_PTS_OFF_TOV', Float),
                Column('OPP_PTS_2ND_CHANCE', Float),
                Column('OPP_PTS_FB', Float),
                Column('OPP_PTS_PAINT', Float),
                Column('DEF_WS', Float)
               )
#est_advanced
est_advanced = Table('est_advanced', metadata,
                     Column('ID', Integer, primary_key=True),
                     Column('PLAYER', String(100)),
                     Column('GP', Integer),
                     Column('W', Integer),
                     Column('L', Integer),
                     Column('MIN', Float),
                     Column('EST_OFFRTG', Float), #name='EST._OFFRTG'),
                     Column('EST_DEFRTG', Float), #name='EST._DEFRTG'),
                     Column('EST_NETRTG', Float), #name='EST._NETRTG'),
                     Column('EST_AST_RATIO', Float), #name='EST._AST_RATIO'),
                     Column('EST_OREB_PCT', Float), #name='EST._OREB%'),
                     Column('EST_DREB_PCT', Float), #name='EST._DREB%'),
                     Column('EST_REB_PCT', Float), #name='EST._REB%'),
                     Column('EST_TO_RATIO', Float), #name='EST._TO_RATIO'),
                     Column('EST_USG_PCT', Float), #name='EST._USG%'),
                     Column('EST_PACE', Float), #name='EST._PACE')
                    )
#misc
misc = Table('misc', metadata,
             Column('IND', Integer, primary_key=True),
             Column('PLAYER', String(100)),
             Column('TEAM', String(50)),
             Column('AGE', Integer),
             Column('GP', Integer),
             Column('W', Integer),
             Column('L', Integer),
             Column('MIN', Float),
             Column('PTS_OFF_TO', Float),
             Column('2ND_PTS', Float),
             Column('FBPS', Float),
             Column('PITP', Float),
             Column('OPP_PTS_OFF_TO', Float),
             Column('OPP_2ND_PTS', Float),
             Column('OPP_FBPS', Float),
             Column('OPP_PITP', Float),
             Column('BLK', Float),
             Column('BLKA', Float),
             Column('PF', Float),
             Column('PFD', Float)
            )

#opponent
opponent = Table('opponent', metadata,
                 Column('ID', Integer, primary_key=True),
                 Column('PLAYER', String(100)), #name='VS_PLAYER'),
                 Column('TEAM', String(50)),
                 Column('GP', Integer),
                 Column('W', Integer),
                 Column('L', Integer),
                 Column('MIN', Float),
                 Column('OPP_FGM', Float),
                 Column('OPP_FGA', Float),
                 Column('OPP_FG_PCT', Float), #name='OPP_FG%'),
                 Column('OPP_3PM', Float),
                 Column('OPP_3PA', Float),
                 Column('OPP_3P_PCT', Float), #name='OPP_3P%'),
                 Column('OPP_FTM', Float),
                 Column('OPP_FTA', Float),
                 Column('OPP_FT_PCT', Float), #name='OPP_FT%'),
                 Column('OPP_OREB', Float),
                 Column('OPP_DREB', Float),
                 Column('OPP_REB', Float),
                 Column('OPP_AST', Float),
                 Column('OPP_TOV', Float),
                 Column('OPP_STL', Float),
                 Column('OPP_BLK', Float),
                 Column('OPP_BLKA', Float),
                 Column('OPP_PF', Float),
                 Column('OPP_PFD', Float),
                 Column('OPP_PTS', Float),
                 Column('plus_minus', Float)
                )

scoring = Table('scoring', metadata,
                Column('ID', Integer, primary_key=True),
                Column('PLAYER', String(100)),
                Column('TEAM', String(50)),
                Column('AGE', Integer),
                Column('GP', Integer),
                Column('W', Integer),
                Column('L', Integer),
                Column('MIN', Float),
                Column('FGA_2PT_PCT', Float), #name='%FGA_2PT'),
                Column('FGA_3PT_PCT', Float), #name='%FGA_3PT'),
                Column('PTS_2PT_PCT', Float), #name='%PTS_2PT'),
                Column('PTS_2PT_MR_PCT', Float), #name='%PTS_2PT_MR'),
                Column('PTS_3PT_PCT', Float), #name='%PTS_3PT'),
                Column('PTS_FBPS_PCT', Float), #name='%PTS_FBPS'),
                Column('PTS_FT_PCT', Float), #name='%PTS_FT'),
                Column('PTS_OFFTO_PCT', Float), #name='%PTS_OFFTO'),
                Column('PTS_PITP_PCT', Float), #name='%PTS_PITP'),
                Column('FG_2PT_AST_PCT', Float), #name='2FG_%AST'),
                Column('FG_2PT_UAST_PCT', Float), #name='2FGM_%UAST'),
                Column('FG_3PT_AST_PCT', Float), #name='3FGM_%AST'),
                Column('FG_3PT_UAST_PCT', Float), #name='3FGM_%UAST'),
                Column('FG_AST_PCT', Float), #name='FGM_%AST'),
                Column('FG_UAST_PCT', Float), #name='FGM_%UAST')
               )

#traditional
traditional = Table('traditional', metadata,
                    Column('ID', Integer, primary_key=True),
                    Column('PLAYER', String(100)),
                    Column('TEAM', String(50)),
                    Column('AGE', Integer),
                    Column('GP', Integer),
                    Column('W', Integer),
                    Column('L', Integer),
                    Column('MIN', Float),
                    Column('PTS', Float),
                    Column('FGM', Float),
                    Column('FGA', Float),
                    Column('FG_PCT', Float), #name='FG%'),
                    Column('3PM', Float),
                    Column('3PA', Float),
                    Column('3P_PCT', Float), #name='3P%'),
                    Column('FTM', Float),
                    Column('FTA', Float),
                    Column('FT_PCT', Float), #name='FT%'),
                    Column('OREB', Float),
                    Column('DREB', Float),
                    Column('REB', Float),
                    Column('AST', Float),
                    Column('TOV', Float),
                    Column('STL', Float),
                    Column('BLK', Float),
                    Column('PF', Float),
                    Column('FP', Float),
                    Column('DD2', Float),
                    Column('TD3', Float),
                    Column('plus_minus', Float)
                   )

# finally usage
usage = Table('player_usage', metadata,
              Column('ID', Integer, primary_key=True),
              Column('PLAYER', String(100)),
              Column('TEAM', String(50)),
              Column('AGE', Integer),
              Column('GP', Integer),
              Column('W', Integer),
              Column('L', Integer),
              Column('MIN', Float),
              Column('USG_PCT', Float), #name='USG%'),
              Column('FGM_PCT', Float), #name='%FGM'),
              Column('FGA_PCT', Float), #name='%FGA'),
              Column('3PM_PCT', Float), #name='%3PM'),
              Column('3PA_PCT', Float), #name='%3PA'),
              Column('FTM_PCT', Float), #name='%FTM'),
              Column('FTA_PCT', Float), #name='%FTA'),
              Column('OREB_PCT', Float), #name='%OREB'),
              Column('DREB_PCT', Float), #name='%DREB'),
              Column('REB_PCT', Float), #name='%REB'),
              Column('AST_PCT', Float), #name='%AST'),
              Column('TOV_PCT', Float), #name='%TOV'),
              Column('STL_PCT', Float), #name='%STL'),
              Column('BLK_PCT', Float), #name='%BLK'),
              Column('BLKA_PCT', Float), #name='%BLKA'),
              Column('PF_PCT', Float), #name='%PF'),
              Column('PFD_PCT', Float), #name='%PFD'),
              Column('PTS_PCT', Float), #name='%PTS')
             )



# create the metadata
metadata.create_all(engine)
print("Tables created successfully.")
# tables should exist now

os.chdir(dir_in)

# creates database versions based off of input folder dir.
parts = dir_in.split("/")
vers = parts[-1]
def dump_database(database, output_file):
    command = f"mysqldump -u root -h localhost {database} > {output_file}"
    subprocess.run(command, shell=True)

# internal functions
def height_to_cm(height):
    feet, inches = map(int, height.split('-'))
    return (feet * 30.48) + (inches * 2.54)

# read in
files = os.listdir()
for x in files: 
    if x == "bio.csv":
        df = pd.read_csv(x,index_col=False,usecols=range(5))
        #fix col names
        df.columns = df.columns.str.strip()
        # convert height to height in cm
        df['HEIGHT'] = df['HEIGHT'].apply(height_to_cm)
        # name cleanup
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df=df.sort_values(by=['PLAYER'])
        # add index for each Player
        df.insert(0, 'ID', range(1,len(df)+1))
        df.to_sql('players', con=engine, if_exists='replace', index=False)

    elif x == "advanced.csv":
        df = pd.read_csv(x, index_col = False)
        #fix col names
        df.columns = df.columns.str.strip()
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df=df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df=df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        #rename first two columns
        #df.columns.values[[0,1]] = ['ID', 'Player']
        #clean up problematic names
        df.rename(columns={
            'AST%': 'ASTP',
            'AST/TO': 'AST_TO',
            'OREB%': 'OREBP',
            'DREB%': 'DREBP',
            'REB%': 'REBP',
            'EFG%': 'EFGP',
            'TS%': 'TSP',
            'USG%': 'USGP'
        }, inplace=True)
        #and write...
        df.to_sql('advanced', con = engine, if_exists='replace', index=False)

    elif x == "defense.csv":
        df = pd.read_csv(x, index_col = False)
        #fix col names
        df.columns = df.columns.str.strip()
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df=df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df=df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        df.rename(columns={
            'DREB%': 'DREB_PCT',
            '%DREB': 'DREB_PCT_TEAM',
            'STL%': 'STL_PCT',
            '%BLK': 'BLK_PCT',
        }, inplace=True)
        # write out
        df.to_sql('defense', con = engine, if_exists='replace', index=False)

    elif x == "estimated-advanced.csv":
        df = pd.read_csv(x, index_col = False)
        #fix col names
        df.columns = df.columns.str.strip()
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df=df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df=df.drop(['IND'], axis = 1)
        # drop last column
        #df = df.iloc[:,:-1]
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        #rename
        df.rename(columns={
            'EST._OFFRTG': 'EST_OFFRTG',
            'EST._DEFRTG': 'EST_DEFRTG',
            'EST._NETRTG': 'EST_NETRTG',
            'EST._AST_RATIO': 'EST_AST_RATIO',
            'EST._OREB%': 'EST_OREB_PCT',
            'EST._DREB%': 'EST_DREB_PCT',
            'EST._REB%': 'EST_REB_PCT',
            'EST._TO_RATIO': 'EST_TO_RATIO',
            'EST._USG%': 'EST_USG_PCT',
            'EST._PACE': 'EST_PACE',
        }, inplace=True)
        # write out
        df.to_sql('est_advanced', con = engine, if_exists='replace', index=False)        

    elif x == "misc.csv":
        df = pd.read_csv(x, index_col = False)
        #fix col names
        df.columns = df.columns.str.strip()
        #fix col names
        df.columns = df.columns.str.strip()
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df=df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df=df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        # write out
        df.to_sql('misc', con = engine, if_exists='replace', index=False)

    elif x == "opponent.csv":
        df = pd.read_csv(x, index_col = False)
        #fix col names
        df.columns = df.columns.str.strip()
        # name fix
        df['VS_PLAYER'] = df['VS_PLAYER'].str.strip()
        # sort by name
        df=df.sort_values(by=['VS_PLAYER'])
        #drop nonsense IND
        df=df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        #names
        df.rename(columns={
            'VS_PLAYER': 'PLAYER',
            'OPP_FG%': 'OPP_FG_PCT',
            'OPP_3P%': 'OPP_3P_PCT',
            'OPP_FT%': 'OPP_FT_PCT',
        }, inplace=True)
        # write out
        df.to_sql('opponent', con = engine, if_exists='replace', index=False)

    elif x == "scoring.csv":
        df = pd.read_csv(x, index_col = False)
        #fix col names
        df.columns = df.columns.str.strip()
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df=df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df=df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        #names
        df.rename(columns={
            '%FGA_2PT': 'FGA_2PT_PCT',
            '%FGA_3PT': 'FGA_3PT_PCT',
            '%PTS_2PT': 'PTS_2PT_PCT',
            '%PTS_2PT_MR': 'PTS_2PT_MR_PCT',
            '%PTS_3PT': 'PTS_3PT_PCT',
            '%PTS_FBPS': 'PTS_FBPS_PCT',
            '%PTS_FT': 'PTS_FT_PCT',
            '%PTS_OFFTO': 'PTS_OFFTO_PCT',
            '%PTS_PITP': 'PTS_PITP_PCT',
            '2FG_%AST': 'FG_2PT_AST_PCT',
            '2FGM_%UAST': 'FG_2PT_UAST_PCT',
            '3FGM_%AST': 'FG_3PT_AST_PCT',
            '3FGM_%UAST': 'FG_3PT_UAST_PCT',
            'FGM_%AST': 'FG_AST_PCT',
            'FGM_%UAST': 'FG_UAST_PCT',
        }, inplace=True)
        # write out
        df.to_sql('scoring', con = engine, if_exists='replace', index=False)

    elif x == "traditional.csv":
        df = pd.read_csv(x, index_col = False)
        #fix col names
        df.columns = df.columns.str.strip()
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df=df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df=df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        #names
        df.rename(columns={
            'FG%': 'FG_PCT',
            '3P%': '3P_PCT',
            'FT%': 'FT_PCT',
        }, inplace=True)
        # write out
        df.to_sql('traditional', con = engine, if_exists='replace', index=False)    

    elif x == "usage.csv":
        df = pd.read_csv(x, index_col = False)
        #fix col names
        df.columns = df.columns.str.strip()
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df=df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df=df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        #name
        
        df.rename(columns={
            'USG%': 'USG_PCT',
            '%FGM': 'FGM_PCT',
            '%FGA': 'FGA_PCT',
            '%3PM': '3PM_PCT',
            '%3PA': '3PA_PCT',
            '%FTM': 'FTM_PCT',
            '%FTA': 'FTA_PCT',
            '%OREB': 'OREB_PCT',
            '%DREB': 'DREB_PCT',
            '%REB': 'REB_PCT',
            '%AST': 'AST_PCT',
            '%TOV': 'TOV_PCT',
            '%STL': 'STL_PCT',
            '%BLK': 'BLK_PCT',
            '%BLKA': 'BLKA_PCT',
            '%PF': 'PF_PCT',
            '%PFD': 'PFD_PCT',
            '%PTS': 'PTS_PCT',
        }, inplace=True)
        # write out
        df.to_sql('usage', con = engine, if_exists='replace', index=False)
#fi


# dump DB
dump_database('NBAPlayerStats2023_24', sqldb + '/NBAPlayerStats2023_24_' + vers + '.sql') 
