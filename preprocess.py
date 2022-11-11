import streamlit as st
import numpy as np
import seaborn as sns
import pandas as pd
import re



def zaman_fonks(string):
    string =string.split(" ")
    date, time = string[0], string[1]
    time = time.split("-")
    time = time[0].strip()
    
    return date + " " + time
    
    

def slash_sil(text):
    return text.split("\n") [0]
    
    
    
    
def preprocess(data):
    
    patern = "\d{1,2}.\d{1,2}.\d{2,4}\s\d{1,2}:\d{2}\s-\s"
    mesajlar = re.split(patern, data)[1:]
    tarihler = re.findall(patern, data)
    
    df = pd.DataFrame({"Kullanıcı_Mesajları" : mesajlar,
                       "Mesaj_Tarihi" : tarihler})
    
    df["Mesaj_Tarihi"] = df["Mesaj_Tarihi"].apply(lambda text: zaman_fonks(text))
    df.rename(columns = {"Mesaj_Tarihi" : "Tarih"}, inplace = True)
    
    kullanicilar = []
    mesajlar = []
    
    for mesaj in df["Kullanıcı_Mesajları"]:
        
        x = re.split("([\w\W]+?):\s", mesaj)
        if x[1:]:
            kullanicilar.append(x[1])
            mesajlar.append(x[2])
            
        else:
            kullanicilar.append("Grup Bildirimi")
            mesajlar.append(x[0])
            
    df["Kullanıcı"] = kullanicilar
    df["Mesaj"] = mesajlar
    
    df["Mesaj"] = df["Mesaj"].apply(lambda text: slash_sil(text))
    
    df = df.drop(["Kullanıcı_Mesajları"], axis = 1)
    df = df[["Mesaj", "Tarih", "Kullanıcı"]]
    
    
    df['Tarih1'] = pd.to_datetime(df['Tarih']).dt.date

    df['Yıl'] = pd.to_datetime(df['Tarih']).dt.year

    df['Ay1'] = pd.to_datetime(df['Tarih']).dt.month

    df['Ay'] = pd.to_datetime(df['Tarih']).dt.month_name()

    df['Gün1'] = pd.to_datetime(df['Tarih']).dt.day

    df['Gün'] = pd.to_datetime(df['Tarih']).dt.day_name()

    df['Saat'] = pd.to_datetime(df['Tarih']).dt.hour

    df['Dakika'] = pd.to_datetime(df['Tarih']).dt.minute
    
    return df