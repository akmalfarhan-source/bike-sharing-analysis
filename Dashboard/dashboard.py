import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

df_day = pd.read_csv(os.path.join(os.path.dirname(__file__), 'main_data.csv'))
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

df_hour = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/hour.csv'))
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

kolom = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
for col in kolom:
    df_day[col] = df_day[col].astype('category')
    df_hour[col] = df_hour[col].astype('category')

df_day['season_label'] = df_day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

st.sidebar.title('Filter Data')
selected_season = st.sidebar.multiselect(
    'Pilih Musim',
    options=['Spring', 'Summer', 'Fall', 'Winter'],
    default=['Spring', 'Summer', 'Fall', 'Winter']
)
df_filtered = df_day[df_day['season_label'].isin(selected_season)]

st.title('🚴 Dashboard Bike Sharing')
st.markdown('Analisis peminjaman sepeda tahun 2011–2012')

col1, col2, col3 = st.columns(3)
col1.metric('Total Peminjaman', f"{df_filtered['cnt'].sum():,}")
col2.metric('Rata-rata Harian', f"{df_filtered['cnt'].mean():.0f}")
col3.metric('Peminjaman Tertinggi', f"{df_filtered['cnt'].max():,}")

st.markdown('---')

st.subheader('Pertanyaan 1: Pola Peminjaman per Jam')
ratajam = df_hour.groupby(['hr', 'workingday'], observed=True)['cnt'].mean().reset_index()
ratajam.columns = ['hr', 'workingday', 'avg_cnt']

fig1, ax1 = plt.subplots(figsize=(10, 4))
for wd, label, color in [(0, 'Hari Libur', 'steelblue'), (1, 'Hari Kerja', 'tomato')]:
    data = ratajam[ratajam['workingday'] == wd]
    ax1.plot(data['hr'], data['avg_cnt'], marker='o', markersize=3, label=label, color=color)
ax1.set_xlabel('Jam')
ax1.set_ylabel('Rata-rata Peminjaman')
ax1.set_xticks(range(0, 24))
ax1.legend()
ax1.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
st.pyplot(fig1)

st.markdown('---')

st.subheader('Pertanyaan 2: Peminjaman per Musim')
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