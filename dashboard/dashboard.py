import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.ticker import FuncFormatter

#
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

#LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    # Pastikan dteday jadi datetime
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

main_data = load_data()

#SIDEBAR FILTER
with st.sidebar:
    st.image("https://raw.githubusercontent.com/mdi-as/bike-sharing-analysis/main/bike_logo.png")
    st.title("Proyek Analisis Data")
    
    #Filter Tahun
    year_options = main_data['yr'].unique()
    selected_year = st.multiselect("Pilih Tahun:", options=year_options, default=year_options)
    
    #Filter Musim
    season_options = main_data['season'].unique()
    selected_season = st.multiselect("Pilih Musim:", options=season_options, default=season_options)

#Filter Logic
filtered_df = main_data[(main_data['yr'].isin(selected_year)) & (main_data['season'].isin(selected_season))]

#JUDUL
st.title("🚲 Bike Rental Analytics Dashboard")
st.markdown("Dashboard ini menyajikan tren penyewaan sepeda berdasarkan tipe pengguna, musim, dan faktor suhu pada tahun 2011 dan 2012.")

#BARIS 1
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rental", value=f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Casual Users", value=f"{filtered_df['casual'].sum():,}")
with col3:
    st.metric("Registered Users", value=f"{filtered_df['registered'].sum():,}")

st.divider()

#BARIS 2: PERBANDINGAN PENGGUNA (GAMBAR 2)
st.subheader("Perbandingan Tipe Pengguna Penyewa Sepeda: Casual vs Registered")

#Grouping data
user_type_rentals = filtered_df.groupby('yr')[['casual', 'registered']].sum().reset_index()
user_type_melted = user_type_rentals.melt(id_vars='yr', var_name='user_type', value_name='total_rentals')

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=user_type_melted, x='yr', y='total_rentals', hue='user_type', palette=['#2E5A88', '#E68A00'], ax=ax)

#Formatter Jutaan
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax.set_xlabel("Tahun")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

#BARIS 3: MUSIM & SUHU (GAMBAR 3 & 4)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Musim (Peak Season)")
    season_rentals = filtered_df.groupby(['yr', 'season'])['cnt'].sum().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.barplot(data=season_rentals, x='yr', y='cnt', hue='season', palette='viridis', ax=ax2)
    ax2.set_ylabel("Total Penyewaan")
    st.pyplot(fig2)

with col_right:
    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Suhu")
    #MENGURUTKAN KATEGORI SUHU
    temp_order = ['Cold', 'Moderate', 'Hot']
    temp_rentals = filtered_df.groupby(['yr', 'temp_category'], observed=False)['cnt'].mean().reset_index()
    temp_rentals['temp_category'] = pd.Categorical(temp_rentals['temp_category'], categories=temp_order, ordered=True)
    
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.barplot(data=temp_rentals, x='temp_category', y='cnt', hue='yr', palette='coolwarm', ax=ax3)
    
    #MENAMBAHKAN LABEL DIATAS BATANG
    for container in ax3.containers:
        ax3.bar_label(container, fmt='%.0f', padding=3)
    
    ax3.set_ylabel("Rata-rata Penyewaan Harian")
    st.pyplot(fig3)

#COPYRIGHT
st.caption(f"Copyright © 2026 - Rafi Maulana Dzaky Bakhtiar CDCC006D6Y1527")
