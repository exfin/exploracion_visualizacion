import pandas as pd


df = pd.read_csv('data/Global_Youtube_Statistics.csv', sep=',', encoding='latin-1')

df = df.drop(['Latitude', 'Longitude'], axis=1)

def cambiar_nombre(lista_index, lista_nuevos):
    for i, idx_nombre in enumerate(lista_index):
        df.loc[idx_nombre,'Youtuber'] = lista_nuevos[i]

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

reemplazo = {'--':'Nombre Local'}

df['Youtuber'] = df['Youtuber'].replace(reemplazo)





