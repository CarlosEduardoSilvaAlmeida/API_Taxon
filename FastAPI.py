from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from functools import lru_cache

DATABASE_URL = 'sqlite:///C:/Users/Carlinhos/Ibama/API/taxon.db'

# Configurar o pool de conexões
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class AcessoBD:
    def __init__(self):
        self.db = SessionLocal()
        self.flag = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def get_levels(self, level, parent_level=None, parent_value=None):
        if level == "subgenus":
            self.flag = True
            query = '''
                SELECT DISTINCT specificEpithet
                FROM taxa
                WHERE genus = :genus
            '''
            params = {'genus': parent_value}
        else:
            query = f'SELECT DISTINCT "{level}" FROM taxa'
            params = {}

            if parent_level and parent_value:
                query += f' WHERE "{parent_level}" = :parent_value'
                params['parent_value'] = parent_value

        result = self.db.execute(text(query), params)
        
        return [row[0] for row in result.fetchall()]
    
    def get_scientific_name(self, genus, species):
        query = '''
            SELECT scientificName
            FROM taxa
            WHERE genus = :genus AND specificEpithet = :species
        '''
        params = {'genus': genus, 'species': species}

        result = self.db.execute(text(query), params)
        
        return result.fetchone()[0]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/levels/{level}", response_class=JSONResponse)
async def get_levels(level: str, parent_level: str = None, parent_value: str = None):
    with AcessoBD() as ac:
        levels = ac.get_levels(level, parent_level, parent_value)
        levels = [lvl for lvl in levels if lvl not in ["Specific Epithet", "Infraspecific Epithet"]]
    return levels

@app.get("/scientific_name/", response_class=JSONResponse)
async def get_scientific_name(genus: str, species: str):
    with AcessoBD() as ac:
        scientific_name = ac.get_scientific_name(genus, species)
    return {"scientific_name": scientific_name}

if __name__ == '__main__': 
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")