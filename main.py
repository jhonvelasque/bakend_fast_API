from fastapi import FastAPI
#creando una istancia de fasAPI
app =FastAPI()
#cambiando el titulo
app.title = 'La apliacion de jhon'
app.version='0.0.1'
@app.get('/',tags=['home'])
def message():
    return "hello world jhon "
    

