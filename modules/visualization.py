import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# CẤU HÌNH GIAO DIỆN 
def setup_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6) 
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

setup_style()
# --- NHÓM BIỂU ĐỒ CƠ BẢN ---

def plot_gender_trend(df):
    data = df.groupby(['Year', 'Sex'])['ID'].nunique().unstack()
    plt.figure(figsize=(10, 6)) 
    plt.plot(data.index, data['M'], marker='.', markersize=8, linewidth=2)
    plt.plot(data.index, data['F'], marker='.', markersize=8, linewidth=2, color='red')
    plt.title('Xu hướng giới tính')
    plt.show()

def plot_top_medals(df, top_n=10):
    df_medals = df[df['Medal'] != 'No Medal']
    # Tính toán top quốc gia 
    top_countries = df_medals['NOC'].value_counts().head(top_n)
    plt.figure(figsize=(10, 6)) 
    plt.bar(top_countries.index, top_countries.values, color=sns.color_palette("viridis", top_n))
    plt.title(f'Top {top_n} quốc gia đạt nhiều huy chương nhất') # Đặt lại tiêu đề cho rõ nghĩa
    plt.xticks(rotation=45)
    plt.ylabel("Số lượng huy chương") 
    plt.show()

def plot_physical_distribution(df):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    sns.histplot(data=df, x='Age', bins=30, ax=axes[0], color='#9b59b6')
    sns.histplot(data=df, x='Height', bins=30, ax=axes[1], color='#3498db')
    sns.histplot(data=df, x='Weight', bins=30, ax=axes[2], color='#2ecc71')
    plt.tight_layout()
    plt.show() 

def plot_physical_comparison_by_sport(df):
    top_sports = df['Sport'].value_counts().head(10).index
    df_top = df[df['Sport'].isin(top_sports)]
    fig, axes = plt.subplots(2, 1, figsize=(12, 12))
    
    sns.boxplot(data=df_top, x='Sport', y='Height', ax=axes[0], hue='Sport', palette='viridis', legend=False)
    axes[0].tick_params(axis='x', rotation=45)
    
    sns.boxplot(data=df_top, x='Sport', y='Weight', ax=axes[1], hue='Sport', palette='magma', legend=False)
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show() 

# --- NHÓM BIỂU ĐỒ NÂNG CAO ---

def plot_host_advantage_china(df):
    years = [1996, 2000, 2004, 2008, 2012, 2016]
    df_chn = df[(df['NOC'] == 'CHN') & (df['Year'].isin(years))]
    medals = df_chn[df_chn['Medal'].notna()].groupby('Year')['Medal'].count()
    plt.figure(figsize=(10, 6)) # Ảnh to
    plt.bar(medals.index.astype(str), medals.values, color='red')
    plt.title('Lợi thế sân nhà TQ')
    plt.show()

def plot_geopolitics_impact(df):
    summer = df[df['Season'] == 'Summer']
    noc_count = summer.groupby('Year')['NOC'].nunique()
    plt.figure(figsize=(10, 6)) # Ảnh to
    plt.plot(noc_count.index, noc_count.values, linewidth=2, color='green')
    plt.title('Số quốc gia tham dự')
    plt.show() 
    
def plot_body_evolution_100m(df):
    subset = df[(df['Event'] == "Athletics Men's 100 metres") & (df['Year'] > 1900)].dropna(subset=['Height', 'Weight'])
    fig, ax1 = plt.subplots(figsize=(10, 6)) # Ảnh to
    sns.regplot(data=subset, x='Year', y='Height', ax=ax1, scatter_kws={'s':20}, line_kws={'lw':2, 'color':'blue'})
    ax2 = ax1.twinx()
    sns.regplot(data=subset, x='Year', y='Weight', ax=ax2, scatter_kws={'s':20, 'color':'orange'}, line_kws={'lw':2, 'color':'orange'})
    plt.show()

# --- VIỆT NAM ---

def plot_vietnam_stats(df):
    df_vn = df[df['NOC'] == 'VIE']
    if df_vn.empty: return
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12)) # Ảnh to
    
    vn_part = df_vn.groupby('Year')['ID'].nunique()
    sns.barplot(x=vn_part.index.astype(str), y=vn_part.values, ax=ax1, color='red')
    ax1.tick_params(axis='x', rotation=90)
    
    top_sports = df_vn['Sport'].value_counts().head(5)
    sns.barplot(x=top_sports.values, y=top_sports.index, ax=ax2, hue=top_sports.index, palette='OrRd', legend=False)
    
    plt.tight_layout()
    plt.show() 

def plot_vietnam_details(df):
    df_vn = df[df['NOC'] == 'VIE']
    medals = df_vn[df_vn['Medal'].isin(['Gold', 'Silver', 'Bronze'])].sort_values('Year')
    cell_text = [[row['Year'], row['Name'], row['Sport'], row['Medal']] for _, row in medals.iterrows()]
    if not cell_text: return
    fig, ax = plt.subplots(figsize=(12, len(cell_text)*0.5 + 2))
    ax.axis('off')
    ax.table(cellText=cell_text, colLabels=["Năm", "VĐV", "Môn", "Huy chương"], loc='center').scale(1, 2)
    plt.show()