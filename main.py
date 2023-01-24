from fastapi import FastAPI
import pandas as pd

app = FastAPI(title= "API to consult Streaming platforms data",
    description= "Amazon, Disney, Hulu and Netflix",   
)

# Cargamos la base de datos al iniciar Uvicorn
@app.on_event('startup')
def startup():
    global DF; global plataformas
    DF = pd.read_csv('Datasets/All_titles.csv')
    plataformas = ['Amazon', 'Hulu', 'Netflix', 'Disney']

# Cargamos información sobre el proyecto
@app.get('/')
async def index():
    return 'PI01 para Henry de Guillermo Fernández'

# Cargamos información sobre la API
@app.get('/about')
async def about():
    return 'API creada con FastAPI y uvicorn'

# En todas las funciones que usen formato str, se eliminan las ' interiores con el comando replace, y se aplica la primer
# letra mayúscula, para que coincida con el Dataset, independiente de cómo lo ingresa el cliente

# Título de más duración, por plataforma y por año:  
# URL para realizar la consulta /get_max_duration(año,'plataforma','[min o season]')
@app.get('/get_max_duration({year},{platform},{min_season})')
async def get_max_duration(
                            year:int,
                            platform:str,
                            min_season:str):
    platform = platform.replace("'","")
    platform = platform.capitalize()
    if platform not in plataformas: return f'Sin datos para {platform}' # Verificacion de plataforma
    min_season = min_season.replace("'","")
    min_season_or = min_season.lower()
    if min_season_or == 'min': min_season = 'Movie'    # Determinamos si es pelicula o serie de acuerdo al parámetro
    elif min_season_or == 'season': min_season = 'TV Show'
    else: return f'Se debe especificar el tipo de duración como "min" o "season"'   # Verificación de tipo
    # Aplicamos una máscara de acuerdo a los parámetros
    Max_duration = DF[(DF.Platform == platform) & (DF.Release_year == year) & ((DF.Type == min_season) )]
    if Max_duration.shape[0] == 0: return f'Sin datos del año {year}'  # Verificacion de año
    # Retornamos el valor del título
    idx = Max_duration.Duration.idxmax()
    return DF.loc[idx].Title, f'{DF.loc[idx].Duration} {min_season_or}s'

# Total de películas y series, por plataforma:
# URL para realizar la consulta /get_count_platform('platform')
#async es una funcion asincrona (ocurre al mismo tiempo) que se acede a la rura
@app.get('/get_count_platform({platform})')
async def get_count_platform(platform:str):
    platform = platform.replace("'","")
    platform = platform.capitalize()
    if platform not in plataformas: return f'Sin datos para {platform}' # Verificacion de plataforma
    Count_platform = DF[(DF.Platform == platform)]  # Aplicamos una máscara de acuerdo al parámetro
    movies = int(Count_platform[Count_platform.Type == 'Movie'].Type.value_counts()[0]) # Contamos la cantidad de ocurrencias
    series = int(Count_platform[Count_platform.Type == 'TV Show'].Type.value_counts()[0])
    # Retornamos el valor en formato str para poder aclarar a qué corresponde cada cantidad
    return platform, f'Movie: {movies}', f'TV Show: {series}'

# Género con mayor ocurrencias, y su plataforma:  
# URL para realizar la consulta /get_listedin('genre')
@app.get('/get_listedin({genre})')
async def get_listedin(genre:str):
    genre = genre.replace("'","")
    genre = genre.capitalize()
    Plataformas, apariciones = list(DF.Platform.unique()), list()   # Creamos una lista con las plataformas, y otra vacía
    for elem in Plataformas:    # Iteramos para cada plataforma
        DF_por_plataforma = DF[(DF.Platform == elem)]   # Aplicamos una máscara de acuerdo al parámetro
        # Creamos una columna que nos indica si se encuentra el parámetro
        DF_por_plataforma['Ind'] = DF_por_plataforma.Listed_in.str.find(genre)
        # Contamos la cantidad de veces que se encuentra el parámetro y lo agregamos a la lista
        apariciones.append(DF_por_plataforma[DF_por_plataforma.Ind != -1].Ind.shape[0])
    if apariciones == [0,0,0,0]: return f'El género {genre} no ha sido encontrado'     # Verificacion de genero
    # Retornamos la plataforma en la que el parámetro  más se repite y la cantidad
    return max(apariciones), Plataformas[apariciones.index(max(apariciones))]

# Actor con mayor ocurrencias, por plataforma y por año:
# URL para realizar la consulta /get_actor('Netflix',2018)
@app.get('/get_actor({platform},{year})')
async def get_actor(
                    platform:str,
                    year:int):
    platform = platform.replace("'","")
    platform = platform.capitalize()
    if platform not in plataformas: return f'Sin datos para {platform}' # Verificacion de plataforma
    actores, repeticiones = list(), list()  # Creamos dos listas vacías para colocar cada actor y la cantidad de veces
    # Aplicamos máscara para obtener una lista de listas de actores, que no tengan nulos
    Cast_list = list(DF[(DF.Platform == platform) & (DF.Release_year == year)].Cast.fillna('Sin_datos'))

    for each in Cast_list:  # Iteramos cada elemento, que es a su vez una lista de actores
        if not(each == 'Sin_datos' or each is None):    # Validamos que tenga datos
            lista = each.split(",") # Separamos por comas, para obtener una lista nueva cuyos elementos sean los actores
            for elem in lista:  # Iteramos sobre esta nueva lista de actores
                elem = elem.strip() # Limpiamos los espacios vacíos
                # Si el actor ya se encuentra en 'actores', entonces sumará 1 en 'apariciones' con el mismo índice
                if elem in actores: 
                    repeticiones[actores.index(elem)] += 1
                # De lo contrario, agregará el actor en 'actores' y 1 en 'apariciones'
                else:    
                    actores.append(elem)
                    repeticiones.append(1)
    if actores == []: return f'Sin datos del año {year}'  # Verificacion de año
    # Retornamos la plataforma, el actor que más se repite en esa plataforma y ese año, y cuántas veces lo hace
    return platform, max(repeticiones), actores[repeticiones.index(max(repeticiones))]