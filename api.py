from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modèle pour les données
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    on_sale: bool

# Base de données simulée
fake_database = {}

@app.get("/")
async def index():
    return {"message": "Bienvenue sur notre API FastAPI !"}

@app.get("/test")
async def test():
    return {"message": "Ceci est un test."}

# Endpoint pour récupérer tous les items
@app.get("/items", response_model=List[Item])
async def get_items():
    return list(fake_database.values())

# Endpoint pour récupérer un item spécifique
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = fake_database.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    return item

# Endpoint pour ajouter un nouvel item
@app.post("/items", response_model=Item)
async def create_item(item: Item):
    if item.id in fake_database:
        raise HTTPException(status_code=400, detail="Item avec cet ID existe déjà")
    fake_database[item.id] = item
    return item

# Endpoint pour mettre à jour un item existant
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    if item_id not in fake_database:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    fake_database[item_id] = updated_item
    return updated_item

# Endpoint pour supprimer un item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in fake_database:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    del fake_database[item_id]
    return {"message": f"L'item avec l'ID {item_id} a été supprimé."}
