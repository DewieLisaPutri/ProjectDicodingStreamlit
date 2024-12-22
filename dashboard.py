import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

st.header(':sparkles: Selamat Datang di Dashboard Sepeda :sparkles:')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_daily_orders_df(df):
    # Mengonversi kolom 'dteday' menjadi tipe datetime jika belum
    df['dteday'] = pd.to_datetime(df['dteday'])
    # Meresample data berdasarkan 'dteday' per hari dan menghitung jumlah penyewaan sepeda (cnt)
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"  # Jumlah penyewaan sepeda per hari
    })
    # Reset index untuk mendapatkan kolom 'dteday' biasa
    daily_orders_df = daily_orders_df.reset_index()
    
    # Menambahkan nama kolom yang lebih jelas
    daily_orders_df.rename(columns={
        "cnt": "total_rentals"
    }, inplace=True)
    
    return daily_orders_df

def create_weekday_weekend_df(df):
    # Menambahkan kolom 'day_type' yang mengelompokkan hari menjadi 'Weekday' atau 'Weekend'
    # Kolom 'weekday' diubah menjadi 'Weekday' jika hari Senin-Jumat (0-4) dan 'Weekend' jika Sabtu-Minggu (5-6)
    df['day_type'] = df['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
    
    # Mengelompokkan berdasarkan 'day_type' dan menghitung jumlah penyewaan sepeda ('cnt')
    by_day_type_df = df.groupby('day_type')['cnt'].sum().reset_index()
    # Mengganti nama kolom untuk kejelasan
    by_day_type_df.rename(columns={'cnt': 'total_rentals'}, inplace=True)
    
    return by_day_type_df

# Membaca dataset
all_df = pd.read_csv("All_Data.csv")

# Mengurutkan data berdasarkan 'dteday'
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# Menentukan rentang tanggal min dan max
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

# Menambahkan logo di sidebar
with st.sidebar:
    st.image("https://github.com/DewieLisaPutri/ProjectDicodingStreamlit/blob/main/image.png")

    # Menentukan rentang tanggal dengan date_input dari Streamlit
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter data berdasarkan rentang tanggal yang dipilih
main_df = all_df[(all_df["dteday"] >= pd.to_datetime(start_date)) & (all_df["dteday"] <= pd.to_datetime(end_date))]

# Menyiapkan dataframe yang diperlukan
daily_orders_df = create_daily_orders_df(main_df)
weekday_weekend_df = create_weekday_weekend_df(main_df)

# Menampilkan total orders
total_orders = daily_orders_df.total_rentals.sum()
st.metric("Total Orders", value=total_orders)


# Plot untuk jumlah penyewaan berdasarkan jenis hari (Weekday vs Weekend)
st.subheader("Jumlah Penyewaan Berdasarkan Jenis Hari (Weekday vs Weekend) ")
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#66b3ff", "#ff9999"]  # Warna untuk Weekday dan Weekend
sns.barplot(
    x="day_type",
    y="total_rentals",
    data=weekday_weekend_df,
    palette=colors,
    ax=ax
)
# Menambahkan judul dan label pada grafik
ax.set_title('Total Penyewaan Sepeda: Weekday vs Weekend', fontsize=20)
ax.set_xlabel('Jenis Hari', fontsize=15)
ax.set_ylabel('Jumlah Penyewa', fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
# Menampilkan grafik pada Streamlit
st.pyplot(fig)


# Menampilkan grafik berdasarkan musim
st.subheader("Jumlah Penyewaan Berdasarkan Musim ")
season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
season_data = {
    'season': [1, 2, 3, 4],
    'cnt': [1200, 2500, 1800, 900]
}
season_df = pd.DataFrame(season_data)
season_df['season'] = season_df['season'].map(season_mapping)

# Mengelompokkan data berdasarkan musim
season_df = season_df.sort_values(by="cnt", ascending=True)

# Warna untuk batang grafik
colors_ = ['#A3C1AD', '#A3C1AD', '#A3C1AD', '#4E84C4']  # Sesuaikan warna

# Plot menggunakan seaborn
plt.figure(figsize=(10, 5))
bar_plot_season = sns.barplot(
    x="cnt",
    y="season",
    data=season_df,
    palette=colors_
)

# Menambahkan label pada setiap batang
for index, value in enumerate(season_df["cnt"]):
    bar_plot_season.text(value + 50, index, str(value), va='center', fontsize=10, color='black')

# Menambahkan judul dan label
plt.title("Total Penyewaan Sepeda Berdasarkan Musim", fontsize=15, loc="center")
plt.xlabel(None)
plt.ylabel(None)
plt.tick_params(axis='y', labelsize=12)
plt.tight_layout()

# Menampilkan grafik di Streamlit
st.pyplot(plt)


