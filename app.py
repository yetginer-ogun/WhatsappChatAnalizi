import streamlit as st
import preprocess
import re
import stats
import matplotlib.pyplot as plt
import numpy as np


st.sidebar.title("WhatsApp Chat Analizi")

dosya = st.sidebar.file_uploader("Bir dosya seçin")

if dosya is not None:
    
    data1 = dosya.getvalue()
    data = data1.decode("utf-8")
    df = preprocess.preprocess(data)
    
    kullanici_listesi = df["Kullanıcı"].unique().tolist()
    try:
        kullanici_listesi.remove("Group Notification")
    except:
        pass
    try:
        kullanici_listesi.remove("Grup Bildirimi")
    except:
        pass
    kullanici_listesi.sort()
    kullanici_listesi.insert(0, "Tümü")
    
    kullanici = st.sidebar.selectbox("Analizi Göster", kullanici_listesi)
    
    st.title("WhatsApp Chat Analizi ", kullanici)
    
    if st.sidebar.button("Analizi Göster"):
        mesaj_sayisi, kelime_sayisi, paylasilan_medya, links = stats.fetchstats(kullanici, df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Toplam Mesaj")
            st.title(mesaj_sayisi)
            
        with col2:
            st.header("Toplam Kelime Sayısı")
            st.title(kelime_sayisi)
            
        with col3:
            st.header("Paylaşılan Medya")
            st.title(paylasilan_medya)
            
        with col4:
            st.header("Paylaşılan Link")
            st.title(links)
            
        if kullanici == "Tümü":
            
            st.title("Etkileşimler")
            etkilesim_sayisi, newdf = stats.fetchetkilesim(df)
            
            fig, ax = plt.subplots()
            col1, col2 = st.beta_columns(2)
           
            with col1:
                ax.bar(etkilesim_sayisi.index, etkilesim_sayisi.values, color = "red")
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)
                
            with col2:
                st.dataframe(newdf)
                
        st.title("Popüler Kelimeler")
        df_img = stats.wordcloud_olustur(kullanici, df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        st.pyplot(fig)
        
        populer_df = stats.populer_kelimeler(kullanici, df)
        fig, ax = plt.subplots()
        ax.barh(populer_df[0], populer_df[1])
        plt.xticks(rotation = "vertical")
        st.title("En Çok Kullanılan Kelimeler")
        st.pyplot(fig)
        
        emoji_df = stats.emoji_fonks(kullanici, df)
        emoji_df.columns = ["Emoji", "Adet"]
        
        st.title("Emoji Analizi")
        
        col1, col2 =st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            eadet = list(emoji_df["Adet"])
            z = [(i/sum(eadet))*100 for i in eadet]
            emoji_df["Kullanım Oranı"] = np.array(z)
            st.dataframe(emoji_df)
            
        st.title("Aylık Aktivite")
        time = stats.aylik_aktivite(kullanici, df)
        fig, ax = plt.subplots()
        ax.plot(time["Tarih"], time["Mesaj"], color = "green")
        plt.xticks(rotation = "vertical")
        plt.tight_layout()
        st.pyplot(fig)
        
        st.title("Aktiviteler")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("En Yoğun Günler")
            yogun_gun = stats.haftalik_aktivite(kullanici, df)
            
            fig, ax = plt.subplots()
            ax.bar(yogun_gun.index, yogun_gun.values, color = "purple")
            plt.xticks(rotation = "vertical")
            plt.tight_layout()
            st.pyplot(fig)
            
        with col2:
            st.header("En Yoğun Aylar")
            yogun_ay = stats.aylik_aktivite2(kullanici, df)
            
            fig, ax = plt.subplots()
            ax.bar(yogun_ay.index, yogun_ay.values, color = "orange")
            plt.xticks(rotation = "vertical")
            plt.tight_layout()
            st.pyplot(fig)
