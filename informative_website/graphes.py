import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("data/ghg.db")
df = pd.read_sql_query("SELECT * from dutchghg", con)
con.close()

# Make visualization for data
plt.figure(1)
plt.plot(df['category'],df['emission'])
plt.title('GHG emissions')
plt.xlabel('Years')
plt.ylabel('Thousand tonnes of CO2 equivalent')
plt.savefig('static/emission.jpg')

plt.figure(2)
plt.plot(df['category'],df['drought'])
plt.title('Cropland exposure to drought')
plt.xlabel('Years')
plt.ylabel('Cropland soil moisture change (%) compared to the baseline climatology (1981-2010)')
plt.savefig('static/drought.jpg')

plt.figure(3)
plt.plot(df['category'],df['extreme_precipitation'])
plt.title('Cropland exposure to extreme precipitation events')
plt.xlabel('Years')
plt.ylabel('Cropland exposed (%), by weeks')
plt.savefig('static/extreme_precipitation.jpg')

plt.figure(4)
plt.plot(df['category'],df['precipitation'])
plt.title('Annual precipitation change')
plt.xlabel('Years')
plt.ylabel('millimetres per year')
plt.savefig('static/precipitation.jpg')

plt.figure(5)
plt.plot(df['category'],df['temperature'])
plt.title('Annual temperature change')
plt.xlabel('Years')
plt.ylabel('degrees Celsius')
plt.savefig('static/temperature.jpg')

plt.figure(6)
plt.plot(df['category'],df['policy'])
plt.title('Policy adoption')
plt.xlabel('Years')
plt.ylabel('numbers of policy adopted')
plt.savefig('static/policy.jpg')

