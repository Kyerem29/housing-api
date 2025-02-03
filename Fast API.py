from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Création de l'instance FastAPI
app = FastAPI()

# Modèle pour la maison
class House(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: int
    total_rooms: int
    total_bedrooms: int
    population: int
    households: int
    median_income: float
    median_house_value: float
    ocean_proximity: str

# Liste pour stocker les maisons (temporaire, à remplacer par une base de données)
houses_db = []

# Exemple d'ajout d'une nouvelle maison
new_house = House(
    longitude=-122.23,
    latitude=37.88,
    housing_median_age=41,
    total_rooms=880,
    total_bedrooms=129,
    population=322,
    households=126,
    median_income=8.3252,
    median_house_value=452600.0,
    ocean_proximity="NEAR BAY"
)

# Ajoute la nouvelle maison à houses_db dès le démarrage
houses_db.append(new_house)

# Route pour récupérer toutes les maisons
@app.get("/houses", response_model=List[House])
def get_houses():
    return houses_db

# Route pour ajouter une maison
@app.post("/houses")
def add_house(house: House):
    houses_db.append(house)
    return {"message": "Maison ajoutée avec succès"}
