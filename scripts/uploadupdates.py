import os
import pandas as pd
import sys
dir_in = sys.argv[1]
sqldb = '/Users/Max_1/Documents/code/NBAStatsSQLsetup/sqldb'
import sqlalchemy
import mysql.connector
from sqlalchemy import create_engine
import subprocess

engine = create_engine('mysql+mysqlconnector:root@localhost')

with engine.connect() as conn:
    conn.execute("CREATE DATABASE IF NOT EXISTS NBAPlayerStats2023-24")
    conn.execute("USE NBAPlayerStats2023-24")
# create our table formats
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
metadata = MetaData()

#player table
players = Table('players', metadata,
                Column('ID', Integer, primary_key=True),
                Column('PLAYER', String(100)),
                Column('TEAM', String(10)),
                Column('AGE', Integer)
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
                 Column('ASTP', Float, name='AST%'),
                 Column('AST_TO', Float),
                 Column('AST_RATIO', Float),
                 Column('OREBP', Float, name='OREB%'),  # OREB%
                 Column('DREBP', Float, name='DREB%'),  # DREB%
                 Column('REBP', Float, name='REB%'),   # REB%
                 Column('TO_RATIO', Float),
                 Column('EFGP', Float, name='EFG%'),   # EFG%
                 Column('TSP', Float, name='TS%'),    # TS%
                 Column('USGP', Float, name='USG%'),   # USG%
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
                Column('DREB_PCT', Float, name='DREB%'),
                Column('DREB_PCT_TOT', Float, name='%DREB'),
                Column('STL', Float),
                Column('STL_PCT', Float, name='STL%'),
                Column('BLK', Float),
                Column('BLK_PCT', Float, name='%BLK'),
                Column('OPP_PTS_OFF_TOV', Float),
                Column('OPP_PTS_2ND_CHANCE', Float),
                Column('OPP_PTS_FB', Float),
                Column('OPP_PTS_PAINT', Float),
                Column('DEF_WS', Float)
               )
# defense
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
                Column('DREB_PCT', Float, name='DREB%'),
                Column('DREB_PCT_TOT', Float, name='%DREB'),
                Column('STL', Float),
                Column('STL_PCT', Float, name='STL%'),
                Column('BLK', Float),
                Column('BLK_PCT', Float, name='%BLK'),
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
                     Column('EST_OFFRTG', Float, name='EST._OFFRTG'),
                     Column('EST_DEFRTG', Float, name='EST._DEFRTG'),
                     Column('EST_NETRTG', Float, name='EST._NETRTG'),
                     Column('EST_AST_RATIO', Float, name='EST._AST_RATIO'),
                     Column('EST_OREB_PCT', Float, name='EST._OREB%'),
                     Column('EST_DREB_PCT', Float, name='EST._DREB%'),
                     Column('EST_REB_PCT', Float, name='EST._REB%'),
                     Column('EST_TO_RATIO', Float, name='EST._TO_RATIO'),
                     Column('EST_USG_PCT', Float, name='EST._USG%'),
                     Column('EST_PACE', Float, name='EST._PACE')
                    )


# create the metadata
metadata.create_all(engine)


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
        df = pd.read_csv(x,index_col=False)
        #filter out bad cols: take first 5 cols
        df = df.iloc[:,:5]
        # convert height to height in cm
        df['HEIGHT'] = df['HEIGHT'].apply(height_to_cm)
        # name cleanup
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df.sort_values(by=['PLAYER'])
        # add index for each Player
        df.insert(0, 'ID', range(1,len(df)+1))
        df.to_sql('players', con=engine, if_exists='replace', index=False)

    elif x == "advanced.csv":
        df = pd.read_csv(x, index_col = False)
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        #rename first two columns
        #df.columns.values[[0,1]] = ['ID', 'Player']
        #clean up problematic names
        #df.rename(columns={
        #    'AST%': 'ASTP',
        #    'AST/TO': 'AST_TO',
        #    'OREB%': 'OREBP',
        #    'DREB%': 'DREBP',
        #    'REB%': 'REBP',
        #    'EFG%': 'EFGP',
        #    'TS%': 'TSP',
        #    'USG%': 'USGP'
        #}, inplace=True)
        #and write...
        df.to_sql('advanced', con = engine, if_exists='replace', index=False)

    elif x == "defense.csv":
        df = pd.read_csv(x, index_col = False)
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        # write out
        df.to_sql('defense', con = engine, if_exists='replace', index=False)

    elif x == "estimated-advanced.csv":
        df = pd.read_csv(x, index_col = False)
        # name fix
        df['PLAYER'] = df['PLAYER'].str.strip()
        # sort by name
        df.sort_values(by=['PLAYER'])
        #drop nonsense IND
        df.drop(['IND'], axis = 1)
        # fix ID to match Bio
        df.insert(0, 'ID', range(1,len(df)+1))
        # write out
        df.to_sql('est_advanced', con = engine, if_exists='replace', index=False)        


#fi

# dump DB
dump_database('NBAPlayerStats2023-24', sqldb + '/NBAPlayerStats2023-24_' + vers + '.sql') 
