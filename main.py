from modules.data_cleaning import clean_data
from modules.data_loader import load_data
from modules.data_scaled import scale_data
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import modules.visualization as viz
df = load_data("data/athlete_events.csv")

df_new = clean_data(df)

viz.plot_vietnam_details(df_new)