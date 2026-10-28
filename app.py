from data.data_processing import df


# print(df['Youtuber'].to_string())


print(df.info())

print(df.loc[df['Country'].isnull(),['Youtuber','Country']].to_string())

print(df['Country'].value_counts())