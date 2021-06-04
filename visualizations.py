import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import scipy

def moving_average(arr, w):
    return np.convolve(arr, np.ones(w), 'valid') / w

path = 'data/discogs_100pg.csv'

discogs = pd.read_csv(path, delimiter=',')

discogs = discogs[discogs.year.notna()]
discogs = discogs[discogs['year'].apply(lambda x: isinstance(x, (str, bytes)))]
discogs['year'] = discogs['year'].str[-4:]
discogs['bool_series']= discogs['year'].str.isdigit()
discogs = discogs[discogs.bool_series == True]
discogs['year'] = discogs['year'].astype(int)

discogs_s = discogs.sort_values(by=['year'])

year_avg = discogs_s.groupby(['year']).price.mean().reset_index()
print(year_avg)

weight1 = 5
weight2 = 10
year_avg_filt1 = moving_average(year_avg['price'],weight1)
year_avg_filt2 = moving_average(year_avg['price'],weight2)

by_year = plt.figure()

ax = by_year.add_subplot(311)
ax.bar(year_avg['year'],year_avg['price'])
ax.set_title('Average Price per Release Year')

ax2 = by_year.add_subplot(312)
ax2.bar(year_avg['year'][weight1-1:],year_avg_filt1)
ax2.set_title('Moving Average - 5 Sample')
ax2.set_ylabel('Price (USD)')

ax3 = by_year.add_subplot(313)
ax3.bar(year_avg['year'][weight2-1:],year_avg_filt2)
ax3.set_title('Moving Average - 10 Sample')
ax3.set_xlabel('Year')
plt.tight_layout(pad=1.0)
plt.show()

# by_year_filt = plt.figure()

# plt.show()
