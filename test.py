import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

df = pd.read_csv('mom_0716.csv')
print(df['name'].tolist())
name = df['official_content'].tolist()
print(name[2795])