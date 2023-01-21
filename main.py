from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
#creando una istancia de fasAPI
app =FastAPI()
#cambiando el titulo
app.title = 'La apliacion de jhon'
app.version='0.0.1'
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
    return HTMLResponse('<h1 style=color:blue> hola mundo </h1>')


@app.get('/movies',tags = ['movies'])
def get_movies():
    return movies

#buscando por id
@app.get('/movies/{id}',tags = ['movies'])
def get_movie(id:int):
    for item in movies:
        if item['id']==id:
            return item
    return []
#utilizando los parametros query 
#solo se tiene que señalarel tipo de parametro
@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category:str,year:int):
    return category ,year

# funcion pra filtrar por sus categorias usando filter 
@app.get('/movies_categorias/', tags = ['movies'])
def get_movies_by_category(category: str):
    #filter(function, iterable)
   return list(filter(lambda item: item['category'] == category , movies))

""" @app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    return [movie for movie in movies if movie['genre'] == category] """
#Utilizando el metodo post
@app.post('/movies',tags=['movies'])
def create_movie(id:int = Body(),title:str= Body(),overview:str= Body(),year:int= Body(),rating:float= Body(),category:str= Body()):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category    
    })
    return movies 
#modificando los datos a partir de encontrar  un dato
@app.put('/movies/{id}',tags=['movies'])
def update_movie(id:int,title:str= Body(),overview:str= Body(),year:int= Body(),rating:float= Body(),category:str= Body()):
    for item in movies:
        if item["id"]==id:
            item["title"]=title,
            item["overview"]=overview,
            item["year"]=year,
            item["rating"]=rating,
            item["category"]=category
            return movies
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
                