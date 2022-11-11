from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji


extract = URLExtract()

def fetchstats(kullanici, df):
    
    if kullanici != "Tümü":
        df = df[df["Kullanıcı"] == kullanici]
        
    mesaj_sayisi = df.shape[0]
    kelimeler = []
    
    for mesaj in df["Mesaj"]:
        kelimeler.extend(mesaj.split())
        
    mdd = df[df["Mesaj"] == "<Medya dahil edilmedi>"]
    
    links = []
    for mesaj in df["Mesaj"]:
        links.extend(extract.find_urls(mesaj))
        
    return mesaj_sayisi, len(kelimeler), mdd.shape[0],len(links)


def fetchetkilesim(df):
    
    df = df[df["Kullanıcı"] != "Group Notification"]
    count = df["Kullanıcı"].value_counts().head()
    
    newdf = pd.DataFrame((df["Kullanıcı"].value_counts()/df.shape[0])*100)
    return count, newdf


def wordcloud_olustur(kullanici, df):
    
    if kullanici != "Tümü":
        df = df[df["Kullanıcı"] == kullanici]
        
    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = "white")
    
    df_wc = wc.generate(df["Mesaj"].str.cat(sep = " "))
    
    return df_wc


def populer_kelimeler(kullanici, df):
    
    y = open("stop_words_turkish.txt", "r")
    stopwords = y.read()
    stopwords = stopwords.split("\n")
    
    if kullanici != "Tümü":
        df = df[df["Kullanıcı"] == kullanici]
        
    temp = df[(df["Kullanıcı"] != "Group Notification") & (df['Mesaj']!='<Medya dahil edilmedi>')]
    
    kelimeler = []
    
    for mesaj in temp["Mesaj"]:
        for kelime in mesaj.lower().split():
            if kelime not in stopwords:
                kelimeler.append(kelime)
                
    populer = pd.DataFrame(Counter(kelimeler).most_common(20))
    return populer


def emoji_fonks(kullanici, df):
    
    if kullanici != "Tümü":
        df = df[df["Kullanıcı"] == kullanici]
        
    emojiler = []
    for mesaj in df["Mesaj"]:
        emojiler.extend([c for c in mesaj if c in emoji.UNICODE_EMOJI["en"]])
        
    emoji_df = pd.DataFrame(Counter(emojiler).most_common(len(Counter(emojiler))))
    return emoji_df


def aylik_aktivite(kullanici, df):
    
    if kullanici != "Tümü":
        df = df[df["Kullanıcı"] == kullanici]
    
    temp = df.groupby(["Yıl", "Ay1", "Ay"]).count()["Mesaj"].reset_index()
    
    time = []
    for i in range(temp.shape[0]):
        time.append(temp['Ay'][i] + "-" + str(temp['Yıl'][i]))
        
    temp['Tarih'] = time
    return temp

    
def haftalik_aktivite(kullanici, df):
    if kullanici != "Tümü":
        df = df[df["Kullanıcı"] == kullanici]
        
    return df["Gün1"].value_counts()


def aylik_aktivite2(kullanici, df):
    if kullanici != "Tümü":
        df = df[df["Kullanıcı"] == kullanici]
        
    return df["Ay"].value_counts()

    
