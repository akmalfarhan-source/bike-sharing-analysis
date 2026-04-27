import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

df_day = pd.read_csv(os.path.join(os.path.dirname(__file__), 'main_data.csv'))
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

kolom = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
for col in kolom:
    df_day[col] = df_day[col].astype('category')

df_day['season_label'] = df_day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

st.sidebar.title('Filter Data')
selected_season = st.sidebar.multiselect(
    'Pilih Musim',
    options=['Spring', 'Summer', 'Fall', 'Winter'],
    default=['Spring', 'Summer', 'Fall', 'Winter']
)
df_filtered = df_day[df_day['season_label'].isin(selected_season)]

st.title('🚴 Dashboard Bike Sharing')
st.markdown('Analisis peminjaman sepeda tahun 2011-2012')

col1, col2, col3 = st.columns(3)
col1.metric('Total Peminjaman', f"{df_filtered['cnt'].sum():,}")
col2.metric('Rata-rata Harian', f"{df_filtered['cnt'].mean():.0f}")
col3.metric('Peminjaman Tertinggi', f"{df_filtered['cnt'].max():,}")

st.markdown('---')

st.subheader('Tren Peminjaman pada Hari Kerja vs Hari Libur')
workingday_avg = df_filtered.groupby('workingday', observed=True)['cnt'].mean().reset_index()
workingday_avg['workingday'] = workingday_avg['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

fig1, ax1 = plt.subplots(figsize=(8, 4))
colors = ['steelblue', 'tomato']
bars = ax1.bar(workingday_avg['workingday'], workingday_avg['cnt'], color=colors, edgecolor='white', width=0.4)
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             f'{bar.get_height():.0f}', ha='center', fontsize=11)
ax1.set_xlabel('Jenis Hari')
ax1.set_ylabel('Rata-rata Peminjaman')
ax1.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
st.pyplot(fig1)

st.markdown('---')

st.subheader('Rata-rata Peminjaman per Musim')
ratamusim = df_filtered.groupby('season_label', observed=True)['cnt'].mean().reset_index()
ratamusim.columns = ['season', 'avg_cnt']

fig2, ax2 = plt.subplots(figsize=(8, 4))
colors = ['#90CAF9', '#FFB74D', '#A5D6A7', '#EF9A9A']
bars = ax2.bar(ratamusim['season'], ratamusim['avg_cnt'], color=colors[:len(ratamusim)], edgecolor='white', width=0.5)
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
             f'{bar.get_height():.0f}', ha='center', fontsize=10)
ax2.set_xlabel('Musim')
ax2.set_ylabel('Rata-rata Peminjaman')
ax2.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
st.pyplot(fig2)

st.markdown('---')
st.caption('Proyek Analisis Data - Akmal Farhan Hidayat')