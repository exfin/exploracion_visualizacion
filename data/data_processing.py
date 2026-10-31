from pathlib import Path

import pandas as pd

# Ruta del CSV relativa a este archivo (no depende del directorio de ejecución)
RUTA_CSV = Path(__file__).parent / 'Global_YouTube_Statistics.csv'

# Leemos el dataset
df = pd.read_csv(RUTA_CSV, sep=',', encoding='latin-1')

# Quitamos las columnas de las coordenadas del país
df = df.drop(['Latitude', 'Longitude'], axis=1)

# Función para limpiar los nombres con carácteres corrompidos
def cambiar_nombre(lista_index, lista_nuevos):
    for i, idx_nombre in enumerate(lista_index):
        df.loc[idx_nombre,'Youtuber'] = lista_nuevos[i]

def reemplazar_pais(df, dicc_paises):
    # mapa_paises es un diccionario: {'Nombre Local': 'México', 'Otro Youtuber': 'España'}
    for youtuber, pais in dicc_paises.items():
        condicion = (df['Youtuber'] == youtuber) & (df['Country'].isnull())
        df.loc[condicion, 'Country'] = pais
    return df


index = [6,55,64,76,91,93,132,145,161,162,165,196,215,220,250,280,320,324,363,382,433,436,441,447,454,462,470,
         480,495,496,507,516,517,547,550,561,571,605,606,624,628,632,637,651,668,669,672,678,690,691,697,698,
         700,707,714,728,739,743,749,752,753,756,784,795,796,810,816,821,828,851,854,866,867,874,875,883,891,
         893, 894,911,914,917,920,923,929,939,945,954,956,975,979,990]

nombres_nuevos = ['Kids Diana Show','Voc','Masha y el Oso (Rusia)','shfa2', 'VladV','One31',
                  'BETER BÖCÜK','DONA mukbang','--','Boram Tube Vlog','toyoraljanahtv',
                  'Kids Roma Show','Junya.','Maroon5','1theK','Peppa Pig Español','Sagawa',
                  'Disney Latinoamerica','Kurzgesagt', 'Genevieve\'s Playhouse','--','Turma da Monica',
                  'Little Angel Español','--','Arab Games Network','RsiamMusic','--','--',
                  'KIMPRO','Jane ASMR','Liziqi','AMARINTV','Al-Remas','Gato Galactico',
                  'With Kids','--','GMMTV OFFICIAL','José Totoy en Español', '--','Kuplinov',
                  'Blippi Español','--','--','--','Hongyu ASMR','Mohamed Ramadan I','--',
                  'Little Angel Español','ISSEI /','--','iTownGamePlay','Thai Ch8','--','--',
                  '--','Planeta das Gemeas','IDEIAS INCRÍVEIS','Boram Tube ToysReview',
                  'Saad Lamjarred','--','Gyan Gaming','--','--','--','Luli Pampín','--','/Atro',
                  'O Que Não Dizer Oficial','Wesley Safadao','The World Adventures','ATHLEAN-X',
                  '--','Kids Line','HUBA','BIBO TOYS','TwinsFromRussia','Knowledge Tv','Peppa Pig em Portugues Brasil',
                  'Ms Yeah','Pastor Antonio Júnior','BIBO KOREA','AlArabiya','--','Melon City Show',
                  'Beyoncé','--','SULGI','Little Baby Bum en Español','--','Gustavo Par','DANIREP','Natan por Ahí']

cambiar_nombre(index, nombres_nuevos)

# Reemplazamos los que no pudieron ser identificados por un nombre en común
reemplazo = {'--':'Nombre Local'}

df['Youtuber'] = df['Youtuber'].replace(reemplazo)

# Borramos las filas de los que no se le sepan el nombre ni el país
filas_borrar = df.loc[(df['Youtuber'] == 'Nombre Local') & (df['Country'].isnull())].index

df = df.drop(filas_borrar)


dicc = {'Music': 'United States', 'Gaming': 'United States',
        'Goldmines':'India','LooLoo Kids - Nursery Rhymes and Children\'s Songs':'United States',
        'Badabun':'Mexico','Bad Bunny':'Puerto Rico','HolaSoyGerman.':'Chile',
        'elrubiusOMG':'Spain','Toys and Colors':'United States','LUCCAS NETO - LUCCAS TOON':'Brazil',
        'PowerKids TV':'India','News':'United States','Ozuna':'Puerto Rico','MrBeast Gaming':'United States',
        'Total Gaming':'India','T-Series Apna Punjab':'India','Techno Gamerz':'India',
        'Desi Music Factory':'Desi Music Factory','WowKidz':'India','SMTOWN':'South Korea',
        'Luis Fonsi':'Puerto Rico','Frost Diamond':'Indonesia','jacksepticeye':'Ireland',
        'Popular on YouTube':'United States','Shorts Break':'India','Aditya Music India':'India',
        'Masha y el Oso':'Russia','Drake':'United States','Goldmines Dishoom':'India',
        'ToyPuddingTV':'South Korea','Gulshan Kalra':'India','NichLmao':'United States',
        'Maroon5':'United States','Fede Vigevani':'Mexico','ZHC':'United States','Las Ratitas':'Spain',
        'ABPLIVE':'India','Chris Brown':'United States','mujjuu___14':'India','Amit Bhadana':'India',
        'Daniel LaBelle':'United States','Goldmines Movies':'India','Venus Entertainment':'Indonesia',
        'NickyJamTV':'United States','Akshay Nagwadiya':'India','KL BRO Biju Rithvik':'India',
        'Like Nastya PRT':'Brazil','Rotana':'Saudi Arabia','Netflix India':'India','Sourav Joshi Vlogs':'India',
        'SMOL':'United States','Khan GS Research Centre':'India','Minecraft - Topic':'United States',
        'Zach King':'United States','Genevieve\'s Playhouse':'United States','Family GamesTV':'United States',
        'Robin Hood Gamer':'Brazil','Troom Troom Es':'United States','Vsauce':'United States',
        'Unbox Therapy':'Canada','Goldmines Great Indian Comedy':'India','Lil Nas X':'United States',
        'Masha e o Urso':'Russia','Cardi B':'United States','Busy Fun Ltd':'India','Ali-A':'United Kingdom',
        'The ACE Family':'United States','Dhar Mann':'United States','Good Mythical Morning':'United States',
        'Bobby chourasiya':'India','Ajay Sharma':'India','BeatboxJCOP':'South Korea','Zuni and Family':'Indonesia',
        'Lil Pump':'United States','Koray Zeynep':'Turkey','PopularMMOs':'United States','Gaby and Alex':'United Kingdom',
        'DeToxoMoroxo':'Mexico','Doggy Doggy Cartoons':'Spain','deepesh zo':'India','Salman Noman':'United Arab Emirates',
        'RCTI - LAYAR DRAMA INDONESIA':'Indonesia','Alfredo Larin':'El Salvador','ExtraPolinesios':'Mexico',
        'Live':'United States','TWICE':'South Korea','sagar kalra (Shorts)':'India','Enes Batur':'Turkey',
        'Kuplinov':'Russia','Super Senya':'United States','Kim Loaiza':'Mexico','Hongyu ASMR':'South Korea',
        'BigSchool':'United States','ZutiGang':'United States','Major Lazer Official':'United States',
        'Hear This Music':'Puerto Rico','NOBRU':'Brazil','Zig & Sharko':'France','Crazy Frog':'Germany',
        'The Dodo':'United States','#Refugio Mental':'Mexico','Dental Digest':'United States','Alexa Rivera':'United States',
        'JD Pantoja':'Mexico','Desi Gamers':'India','Stray Kids':'South Korea','Ei Nerd':'Brazil',
        'Ian Boggs':'United States','Knowledge Tv':'Nigeria','Rauw Alejandro':'Puerto Rico','Troom Troom India':'India',
        'Ian Lucas':'Argentina','Jass Records':'India','Ja Mill':'Philippines','Troom Troom PT':'Brazil','Troom Troom Indonesia':'Indonesia',
        'Hero Movies 2023':'United States','TKOR':'United States','ANNA KOVA':'Russia','BRIGHT SIDE':'Cyprus'}
df = reemplazar_pais(df, dicc)




