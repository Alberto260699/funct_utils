import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns #statistical data visualization

data = {
    'CHN': {'COUNTRY': 'China', 'POP': 1_398.72, 'AREA': 9_596.96,
            'GDP': 12_234.78, 'CONT': 'Asia'},
    'IND': {'COUNTRY': 'India', 'POP': 1_351.16, 'AREA': 3_287.26,
            'GDP': 2_575.67, 'CONT': 'Asia', 'IND_DAY': '1947-08-15'},
    'USA': {'COUNTRY': 'US', 'POP': 329.74, 'AREA': 9_833.52,
            'GDP': 19_485.39, 'CONT': 'N.America', 'IND_DAY': '1776-07-04'},
    'IDN': {'COUNTRY': 'Indonesia', 'POP': 268.07, 'AREA': 1_910.93,
            'GDP': 1_015.54, 'CONT': 'Asia', 'IND_DAY': '1945-08-17'},
    'BRA': {'COUNTRY': 'Brazil', 'POP': 210.32, 'AREA': 8_515.77,
            'GDP': 2_055.51, 'CONT': 'S.America', 'IND_DAY': '1822-09-07'},
    'PAK': {'COUNTRY': 'Pakistan', 'POP': 205.71, 'AREA': 881.91,
            'GDP': 302.14, 'CONT': 'Asia', 'IND_DAY': '1947-08-14'},
    'NGA': {'COUNTRY': 'Nigeria', 'POP': 200.96, 'AREA': 923.77,
            'GDP': 375.77, 'CONT': 'Africa', 'IND_DAY': '1960-10-01'},
    'BGD': {'COUNTRY': 'Bangladesh', 'POP': 167.09, 'AREA': 147.57,
            'GDP': 245.63, 'CONT': 'Asia', 'IND_DAY': '1971-03-26'},
    'RUS': {'COUNTRY': 'Russia', 'POP': 146.79, 'AREA': 17_098.25,
            'GDP': 1_530.75, 'IND_DAY': '1992-06-12'},
    'MEX': {'COUNTRY': 'Mexico', 'POP': 126.58, 'AREA': 1_964.38,
            'GDP': 1_158.23, 'CONT': 'N.America', 'IND_DAY': '1810-09-16'},
    'JPN': {'COUNTRY': 'Japan', 'POP': 126.22, 'AREA': 377.97,
            'GDP': 4_872.42, 'CONT': 'Asia'},
    'DEU': {'COUNTRY': 'Germany', 'POP': 83.02, 'AREA': 357.11,
            'GDP': 3_693.20, 'CONT': 'Europe'},
    'FRA': {'COUNTRY': 'France', 'POP': 67.02, 'AREA': 640.68,
            'GDP': 2_582.49, 'CONT': 'Europe', 'IND_DAY': '1789-07-14'},
    'GBR': {'COUNTRY': 'UK', 'POP': 66.44, 'AREA': 242.50,
            'GDP': 2_631.23, 'CONT': 'Europe'},
    'ITA': {'COUNTRY': 'Italy', 'POP': 60.36, 'AREA': 301.34,
            'GDP': 1_943.84, 'CONT': 'Europe'},
    'ARG': {'COUNTRY': 'Argentina', 'POP': 44.94, 'AREA': 2_780.40,
            'GDP': 637.49, 'CONT': 'S.America', 'IND_DAY': '1816-07-09'},
    'DZA': {'COUNTRY': 'Algeria', 'POP': 43.38, 'AREA': 2_381.74,
            'GDP': 167.56, 'CONT': 'Africa', 'IND_DAY': '1962-07-05'},
    'CAN': {'COUNTRY': 'Canada', 'POP': 37.59, 'AREA': 9_984.67,
            'GDP': 1_647.12, 'CONT': 'N.America', 'IND_DAY': '1867-07-01'},
    'AUS': {'COUNTRY': 'Australia', 'POP': 25.47, 'AREA': 7_692.02,
            'GDP': 1_408.68, 'CONT': 'Oceania'},
    'KAZ': {'COUNTRY': 'Kazakhstan', 'POP': 18.53, 'AREA': 2_724.90,
            'GDP': 159.41, 'CONT': 'Asia', 'IND_DAY': '1991-12-16'}
}

columns = ('COUNTRY', 'POP', 'AREA', 'GDP', 'CONT', 'IND_DAY')

df = pd.DataFrame(data, columns).T
#df.loc['RUS','CONT']='Asia'
print(df)
cont_df = df[['CONT','COUNTRY']].groupby('CONT').count()
cont_df['Total'] = cont_df['COUNTRY'].sum()
cont_df['%'] = cont_df['COUNTRY']*100/cont_df['Total']
print(cont_df)
cont_df.plot(kind='bar')
plt.show()


df.shape() #riporta numero di righe e colonne
df.head() #riporta le prime 5 righe
df.tail(10) #ripota le ultime 10 righe
df['COUNTRY'] #mostra i dati della sola colonna
df['COUNTRY'].value_counts() #conteggia i valori che si ripetono
df[['CONT','COUNTRY']] #identicamente a sopra ma riporta due colonne
'''iloc e loc fanno la stessa cosa, iloc seleziona con numeri, loc con nomi'''
df.loc['RUS','CONT']='Asia'
df.iloc[0]='Asia' #righa selezionata [0,:] ":" è implicito
''' puoi anche variare quello che c'è tra le quadre [row,col]'''
df.descibe() #restituisce una summary del dataframe
df.dtypes() #restituisce il tipo di valore
df.isnull() #detect missing values
df.isnull().sum() #riporta il complesso dei dati mancanti
df.drop('nome_col', axis=x, inplace=True)
''' axis=0 per indicare le righe
    axis=1 per indicare le colonne
    axis=2 in 3D indica la profondità'''
#se non vuoi mettere inplace=True
df=df.drop('nome_col', axis=x)
#drop more columns
df.drop(columns=[col1,col2],axis=x,inplace=True)
df.corr() #riporta le correlazioni che ci sono tra le diverse colonne
cont_df = df[['CONT','COUNTRY']].groupby('CONT').count().to_frame(name='nome_col') #to_frame per trasformarlo in una tabella
cont_df = df[['CONT','COUNTRY']].groupby('CONT').mean() #per fare la media
cont_df = df[['CONT','COUNTRY']].groupby('CONT').sum(ascending = False) #per fare la somma, in ordine decrescente