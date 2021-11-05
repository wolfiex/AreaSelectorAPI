#!/usr/bin/env python
# coding: utf-8

# !pip install pysqlite
import re,os
import pandas as pd

import sqlite3
conn = sqlite3.connect('postcodes.db')
cursor = conn.cursor()

''' get the postcodes file '''

filename = './PCD_OA_LSOA_MSOA_LAD_FEB20_UK_LU.zip'
# yes we can read zip files directly
df = pd.read_csv(filename, compression='zip', header=0, sep=',', quotechar='"',  encoding='latin-1')
df['pcd']= [i.replace(' ','') for i in df.pcds]
# df['id'] = [i.split()[0] for i in df.pcds]
df.head(2)


lad = list(enumerate(i for i in set(df.ladcd) if str(i)[1:]!= ['99999999']))[1:]
rlad = dict([[j,i] for i,j in lad])

conn.execute('''DROP TABLE IF EXISTS LAD; ''')
conn.execute('''
                 CREATE TABLE LAD
                 (
                    ID           INT         PRIMARY KEY,
                    CODE         CHAR(9)     NOT NULL
                 );
            ''')


conn.executemany('INSERT INTO LAD (ID,CODE) VALUES (?,?)', lad)
conn.commit()


lsoa = list(enumerate(i for i in set(df.lsoa11cd) if str(i)[1:]!= ['99999999']))[1:]
rlsoa = dict([[j,i] for i,j in lsoa])



parent = df[['lsoa11cd','lsoa11cd', 'ladcd']].dropna()
parent.columns=[0,1,2]
parent[0] = [rlsoa[i] for i in parent[0]]
parent = parent.drop_duplicates().sort_values(0)



conn.execute('''DROP TABLE IF EXISTS LSOA; ''')
conn.execute('''
                 CREATE TABLE LSOA
                 (
                    ID           INTEGER     KEY,
                    CODELAD      CHAR(9)     NOT NULL,
                    CODE         CHAR(9)     NOT NULL
                    
                 );
            ''')

conn.executemany('INSERT INTO LSOA (ID,CODE,CODELAD) VALUES (?,?,?)', parent.values)
conn.commit()



conn.execute('SELECT * from LSOA LIMIT 3').fetchall()


# In[247]:


cols = ['pcd' ,'pcds','ladcd']
postlad = df[cols].dropna()
postlad['ladcd'] = [rlad[i] for i in postlad['ladcd']]
# postlad['lsoa11cd'] = [rlsoa[i] for i in postlad['lsoa11cd']]

vals = postlad.groupby(cols).first().index.values

conn.execute('''DROP TABLE IF EXISTS POSTAREA; ''')
conn.execute('''
                 CREATE TABLE POSTAREA
                 (
                    PSELECT        CHAR(7)     PRIMARY KEY,
                    POST           CHAR(8)     NOT NULL,
                    IDLSOA         INTEGER     NOT NULL
                 );
            ''')


conn.executemany('INSERT INTO POSTAREA (PSELECT,POST,IDLSOA) VALUES (?,?,?)', vals)
conn.commit()


vals


# In[248]:


# conn.execute('SELECT * from POSTAREA WHERE POST LIKE "YO%" LIMIT 3;').fetchall()
# conn.execute('SELECT POST,IDLSOA from POSTAREA WHERE PSELECT LIKE "YO104%" LIMIT 3;').fetchall()




numericre = re.compile(r'\b\d.*|[^\w\s]')


lsoanames = [[numericre.sub('',str(i[0])),i[1]] for i in  df[['lsoa11nm','ladcd']].dropna().drop_duplicates().values]
lsoanames = pd.DataFrame(lsoanames)
lsoanames = lsoanames[[str(i)[1:]!='99999999' for i in lsoanames[1]]]
lsoanames[1] = [rlad[i] for i in lsoanames[1]]
lsoanames[2]=False
lsoanames


print('using LAD as LSOA overlap')
ladnames = pd.DataFrame(df[['ladnm','ladcd']].dropna().drop_duplicates().values).dropna()
# ladnames[0] = [ i + ' (region)' if i in lsoanames[0] else i  for i in ladnames[0] ]
ladnames = ladnames[[str(i)[1:]!='99999999' for i in ladnames[1]]]
ladnames[1] = [rlad[i] for i in ladnames[1]]
ladnames[2]=True
ladnames



nameslist = pd.concat([lsoanames,ladnames]).drop_duplicates()


maxlength = max([len(i) for i in nameslist[0]])


nameslist = nameslist.sort_values(0)
# nameagg = nameslist.groupby([0,2]).agg(tuple).reset_index()
# nameagg[1] = nameagg[1].apply(sqlite3.Binary)


conn.execute('''DROP TABLE IF EXISTS namelist; ''')
conn.execute('''
                 CREATE TABLE namelist
                 (
                    NAME        CHAR(%s)     NOT NULL,
                    CODE        int          NOT NULL,
                    LAD         logical      NOT NULL
                 );
            '''%maxlength)


conn.executemany('INSERT INTO namelist (NAME,CODE,LAD) VALUES (?,?,?)', nameslist.values)
conn.commit()


conn.close()

