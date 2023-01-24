from fastapi import FastAPI, Body ,Path ,Query
#path sirve para los parametros de ruta 
from fastapi.responses import HTMLResponse
#fiel es una clase de validacion
from  pydantic import BaseModel,Field
from typing import Optional
#creando una istancia de fasAPI
app =FastAPI()
#cambiando el titulo
app.title = 'La apliacion de jhon'
app.version='0.0.1'
#todos estos cambio lo puedes ver mas rapidoe en el metodo post 
class Movie(BaseModel):
    id:Optional[int]=None
    #id:int |None=None ->otraforma de poner un atributo opcional 
    #min_length son loscaracteres minimos
    #max_length son los caracteres maximos
    title :str=Field(min_length=5,max_length =15)
    overview:str=Field(min_length=5,max_length =15)
    #le > menor igual
    #ge -> mayor igua;
    year : int= Field(le=2000)
    rating:float= Field(ge=0,le=10)
    category : str=Field(min_lengt=2)
    #nota la clase Config es UN valor fijo que no debe cambiar al igual que la key example
    class Config :
        schema_extra={
            'example':{
            'title':'mi pelicula',
            'overview':'la dewscripcion de la pelicula',
            'year':2022,
            'rating':9.8,
            'category':'Accion'
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar1',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } ,
    {
        'id': 2,
        'title': 'Avatar2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2022',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]
#@app.put('/ruta/{parametro necesario}',tags=['a que etiqueta pertenece'])
@app.get('/', tags=['home'])
def home():
    return HTMLResponse('<h1 style=color:blue> hola mundo </h1>''<br style=color:blue>mi primera api estoy feliz</br>')



@app.get('/movies',tags = ['movies'])
def get_movies():
    return movies

#buscando por id
@app.get('/movies/{id}',tags = ['movies'])
def get_movie(id: int = Path(ge=1,le=2000)):
    for item in movies:
        if item['id']==id:
            return item
    return []

#utilizando los parametros query 
#solo se tiene que señalarel tipo de parametro
@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category:str, year:int):
    return category ,year

# funcion pra filtrar por sus categorias usando filter 
@app.get('/movies_categorias/', tags = ['movies'])
def get_movies_by_category(category: str=Query(min_length=5, max_length=20)):
    #filter(function, iterable)
   return list(filter(lambda item: item['category'] == category , movies))

""" @app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    return [movie for movie in movies if movie['genre'] == category] """
#Utilizando el metodo post que nos permite registrar nuestros datos
@app.post('/movies',tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies 
#modificando los datos a partir de encontrar  un dato
@app.put('/movies/{id}',tags=['movies'])
def update_movie(id:int,movie:Movie):
    for item in movies:
        if item["id"]==id:
            item["title"]=movie.title,
            item["overview"]=movie.overview,
            item["year"]=movie.year,
            item["rating"]=movie.rating,
            item["category"]=movie.category
            return movies
@app.put('/movies/{id}', tags=['movies'])
#otra forma
# async def update_movie(id: int, movie: Movie):

#     for index, item in enumerate(movies):
#         if item["id"] == id:
#             movies[index].update(movie)
#             movies[index]["id"] = id
#             return movies[index]
    
#eliminando a partir del id
@app.delete('/movies/{id}',tags=['movies'])
def delete_movies(id:int):
    for item in movies:
        if item in movies:
            if item["id"]==id:
                #funcion de lista para eliminar un elemento
                movies.remove(item)
                return movies
            else :
                return "no se encontro la pelicula"
                