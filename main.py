from fastapi import FastAPI, Body ,Path ,Query
#path sirve para los parametros de ruta 
from fastapi.responses import HTMLResponse ,JSONResponse
#fiel es una clase de validacion
from  pydantic import BaseModel,Field
from typing import Optional ,List
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
    overview:str=Field(min_length=1,max_length =100)
    #le > (maximo)menor igual
    #ge -> (minimo)mayor igual;
    year : int= Field(ge=2000)
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



@app.get('/movies',tags = ['movies'],response_model=List[Movie])
def get_movies()->List[Movie]:
    #IMPORTANTE ESPECIFICAR EL CONTENIDO
    return JSONResponse(content=movies)

#buscando por id
@app.get('/movies/{id}',tags = ['movies'],response_model=Movie)
#devolviendo una pelicula
def get_movie(id: int = Path(ge=1,le=2000))-> Movie:
    for item in movies:
        if item['id']==id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])


#utilizando los parametros query 
#solo se tiene que señalarel tipo de parametro

@app.get('/movies/',tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category:str=Query(min_length=5,max_length=25))->List[Movie]:
    data=[item for item in movies if item['category']==category]
    return JSONResponse(content=data)

# funcion pra filtrar por sus categorias usando filter 
@app.get('/movies_categorias/', tags = ['movies'])
def get_movies_by_category(category: str=Query(min_length=5, max_length=20)):
    #filter(function, iterable)
   return list(filter(lambda item: item['category'] == category , movies))



#Utilizando el metodo post que nos permite registrar nuestros datos
@app.post('/movies',tags=['movies'],response_model=dict)
def create_movie(movie: Movie)-> dict:
    movies.append(movie)
    return JSONResponse(content={'message':'se registro la pelicula'}) 
#modificando los datos a partir de encontrar  un dato
#implementando los esquemas


@app.put('/movies/{id}',tags=['movies'],response_model=dict)
def update_movie(id:int,movie:Movie)->dict:
    for item in movies:
        if item["id"]==id:
            item["title"]=movie.title,
            item["overview"]=movie.overview,
            item["year"]=movie.year,
            item["rating"]=movie.rating,
            item["category"]=movie.category
            return JSONResponse(content={'message':'se modifico la pelicula '})
#@app.put('/movies/{id}', tags=['movies'])
#otra forma
# async def update_movie(id: int, movie: Movie):

#     for index, item in enumerate(movies):
#         if item["id"] == id:
#             movies[index].update(movie)
#             movies[index]["id"] = id
#             return movies[index]
    
#eliminando a partir del id
@app.delete('/movies/{id}',tags=['movies'],response_model=dict)
def delete_movies(id:int)->dict:
    for item in movies:
        if item in movies:
            if item["id"]==id:
                #funcion de lista para eliminar un elemento
                movies.remove(item)
                return movies
            else :
                return "no se encontro la pelicula"