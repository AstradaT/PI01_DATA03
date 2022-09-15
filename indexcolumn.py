import pandas as pd
import numpy as np


df = pd.read_csv('Datasets/lap_times/lap_times5.csv')
df['ix'] = np.arange(399999,399999+len(df.index))
#print(df)
df.to_csv('Datasets/lap_times/lap_times5.csv', index=False)