from fastapi import FastAPI
from fastapi.responses import HTMLResponse
#creando una istancia de fasAPI
app =FastAPI()
#cambiando el titulo
app.title = 'La apliacion de jhon'
app.version='0.0.1'
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } ,
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]

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

@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category:str,year:int):
    return category ,year