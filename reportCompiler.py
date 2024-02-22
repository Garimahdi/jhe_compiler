import pandas as pd
import numpy as np
from openpyxl import load_workbook
import datetime

def modeller(dataset, user):
    # Load all necessary dataset
    df_raw = pd.read_excel(r"D:\Astragraphia\BO1\Hexindo\Report Pemakaian\{}".format(dataset))
    df_user = pd.read_excel(r"D:\Astragraphia\BO1\Hexindo\Report Pemakaian\{}".format(user))

    # Get all columns from all dataset
    cr = list(df_raw.columns)
    cu = list(df_user.columns)
    
    # Data modelling

    # Convert user data as string
    df_user = df_user.astype({cu[0]:str})

    # Model code column reformat as 2 columns
    list_0 = []
    for i in df_raw[cr[1]]:
        for a in i.split('_'):
            list_0.append(a)

    model_code = list_0[::2]
    iden = list_0[1::2]

    df_raw[cr[1].split('_')[0]] = model_code
    df_raw[cr[1].split('_')[1]] = iden

    df_raw.drop(columns=[cr[1],cr[7],cr[13],cr[14]], inplace=True)
    
    # Rearrange columns
    cf = list(df_raw.columns)
    df_final = df_raw[[cf[0],cf[11],cf[12],cf[1],cf[2],cf[3],cf[4],cf[5],cf[6],cf[7],cf[8],cf[9],cf[10]]]
    
    # Mapping staff and their depts respectively
    users = df_user[[cu[0],cu[2]]]
    depts = df_user[[cu[0],cu[1]]]

    map_users = dict(users.values)
    map_depts = dict(depts.values)

    df_final['User Name'] = df_final[cf[0]].map(map_users)
    df_final['Dept'] = df_final[cf[0]].map(map_depts)
    cff = list(df_final.columns)

    df_final = df_final[[
        cff[0],
        cff[13],
        cff[14],
        cff[1],
        cff[2],
        cff[3],
        cff[4],
        cff[5],
        cff[6],
        cff[7],
        cff[8],
        cff[9],
        cff[10],
        cff[11],
        cff[12]
    ]]
    
    return df_final

def paperClr(df,c):
    paper_size = [
    (df[c[24]] > 0) | (df[c[24+7]] > 0),
    (df[c[25]] > 0) | (df[c[25+7]] > 0),
    (df[c[26]] > 0) | (df[c[26+7]] > 0),
    (df[c[27]] > 0) | (df[c[27+7]] > 0),
    (df[c[28]] > 0) | (df[c[28+7]] > 0),
    (df[c[29]] > 0) | (df[c[29+7]] > 0),
    (df[c[30]] > 0) | (df[c[30+7]] > 0),
    (
        (df[c[24]] == 0)&
        (df[c[25]] == 0)&
        (df[c[26]] == 0)&
        (df[c[27]] == 0)&
        (df[c[28]] == 0)&
        (df[c[29]] == 0)&
        (df[c[30]] == 0)&
        (df[c[24+7]] == 0)&
        (df[c[25+7]] == 0)&
        (df[c[26+7]] == 0)&
        (df[c[27+7]] == 0)&
        (df[c[28+7]] == 0)&
        (df[c[29+7]] == 0)&
        (df[c[30+7]] == 0)
        )
    ]
    paper_desc = [
        'A4', 'JIS B4', 'A3', 'Letter', 'Legal', 'Ledger', 'Other', 'No Printing'
    ]

    df['Paper Size'] = np.select(paper_size, paper_desc)
    #df['Colour Output'] = np.where(
    #    (df[c[92]] != 0)&(df[c[91]] == 0), 'Black & White','Color')

    mesin = df.loc[df['Paper Size'] != 'No Printing']
    return mesin

def jheTranslator(ina, eng, colNameIna, colNameEng, colNum):
    try:
        for a,b in zip(colNameIna, colNameEng):
            ina.rename(columns={a:b}, inplace=True)
    except Exception as e:
        print("ERROR COLUMN RENAME PROCESS:", e)
    
    inaJobType = np.array(list(ina[colNameEng[colNum]].unique()))
    arrIdx = [1,0]
    for i in range(2,len(inaJobType)):
        arrIdx.append(i)
    inaUni = inaJobType[arrIdx]
    
    try:
        for c,d in zip(inaUni, list(eng[colNameEng[colNum]].unique())):
            ina.replace({colNameEng[colNum]:{c:d}}, inplace=True)
    except Exception as e:
        print("ERROR JOB TYPE TRANSLATION PROCESS:", e)
        
    return ina

def userDeptMapping(df, dictUser, dictDept, c):
    df['Nama'] = df[c[12]].map(dictUser)
    df['Dept'] = df[c[12]].map(dictDept)
    df[c[12]].fillna(0, inplace=True)
    return df

def filler(df, c, floor):
    df[c[12]] = df[c[12]].astype(str)
    df['Nama'] = df['Nama'].fillna(df[c[12]])
    df['Dept'] = df['Dept'].fillna(str(floor))
    df['Location'] = floor
    df_prep = df[[
        c[12],
        'Nama',
        'Dept',
        'Location',
        c[7],
        'Paper Size',
        c[91],
        c[92]
    ]]
    return df_prep

def fillerTrans(compiledFx, compiledFf):
    cx = list(compiledFx.columns)
    cf = list(compiledFf.columns)
    for old, new in zip(cx, cf):
        compiledFx.rename(columns={old:new}, inplace=True)
    return compiledFx

def mergeData(d1,d2,d3=None,d4=None,d5=None,d6=None,d7=None,d8=None,d9=None,d10=None):
    if (d3 is None) and (d4 is None) and (d5 is None) and (d6 is None) and (d7 is None) and (d8 is None) and (d9 is None) and (d10 is None):
        merged = pd.concat([d1, d2])
        
    elif (d3 is not None) and (d4 is None) and (d5 is None) and (d6 is None) and (d7 is None) and (d8 is None) and (d9 is None) and (d10 is None):
        merged = pd.concat([d1,d2,d3])
        
    elif (d3 is not None) and (d4 is not None) and (d5 is None) and (d6 is None) and (d7 is None) and (d8 is None) and (d9 is None) and (d10 is None):
        merged = pd.concat([d1,d2,d3,d4])
    
    elif (d3 is not None) and (d4 is not None) and (d5 is not None) and (d6 is None) and (d7 is None) and (d8 is None) and (d9 is None) and (d10 is None):
        merged = pd.concat([d1,d2,d3,d4,d5])
        
    elif (d3 is not None) and (d4 is not None) and (d5 is not None) and (d6 is not None) and (d7 is None) and (d8 is None) and (d9 is None) and (d10 is None):
        merged = pd.concat([d1,d2,d3,d4,d5,d6])
        
    elif (d3 is not None) and (d4 is not None) and (d5 is not None) and (d6 is not None) and (d7 is not None) and (d8 is None) and (d9 is None) and (d10 is None):
        merged = pd.concat([d1,d2,d3,d4,d5,d6,d7])
        
    elif (d3 is not None) and (d4 is not None) and (d5 is not None) and (d6 is not None) and (d7 is not None) and (d8 is not None) and (d9 is None) and (d10 is None):
        merged = pd.concat([d1,d2,d3,d4,d5,d6,d7,d8])
        
    elif (d3 is not None) and (d4 is not None) and (d5 is not None) and (d6 is not None) and (d7 is not None) and (d8 is not None) and (d9 is not None) and (d10 is None):
        merged = pd.concat([d1,d2,d3,d4,d5,d6,d7,d8,d9])
        
    elif (d3 is not None) and (d4 is not None) and (d5 is not None) and (d6 is not None) and (d7 is not None) and (d8 is not None) and (d9 is not None) and (d10 is not None):
        merged = pd.concat([d1,d2,d3,d4,d5,d6,d7,d8,d9,d10])
    
    return merged