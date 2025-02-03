from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base
import subprocess

# 🔧 Connexion PostgreSQL
DATABASE_URL = "postgresql://kevin:KV1292005@db:5432/housing_db?client_encoding=utf8"

# 🔥 Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 📌 Modèle SQLAlchemy pour la table "houses"
class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    housing_median_age = Column(Integer, nullable=False)
    total_rooms = Column(Integer, nullable=False)
    total_bedrooms = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)
    households = Column(Integer, nullable=False)
    median_income = Column(Float, nullable=False)
    median_house_value = Column(Float, nullable=False)
    ocean_proximity = Column(String, nullable=False)

# ✅ Création des tables si elles n'existent pas encore
def init_db():
    print("🔄 Initialisation de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès !")

# 🚀 Exécuter les migrations Alembic automatiquement
def run_migrations():
    print("🔄 Exécution des migrations Alembic...")
    try:
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", "Initial Migration"], check=True)
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Migrations appliquées avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")

# ➕ Ajouter une maison dans la base
def add_house(session, house_data):
    new_house = House(**house_data)
    session.add(new_house)
    session.commit()
    print(f"🏡 Maison ajoutée : {new_house}")

# 📜 Afficher toutes les maisons
def list_houses(session):
    houses = session.query(House).all()
    print("\n📜 Liste des maisons dans la base :")
    for house in houses:
        print(f"- {house.id}: {house.median_house_value}€ près de {house.ocean_proximity}")

# 🚀 Initialisation et tests
if __name__ == "__main__":
    init_db()
    run_migrations()

    # Démarrer une session
    session = SessionLocal()

    # ➕ Ajouter des maisons test
    house_data = [
        {
            "longitude": -122.23,
            "latitude": 37.88,
            "housing_median_age": 41,
            "total_rooms": 880,
            "total_bedrooms": 129,
            "population": 322,
            "households": 126,
            "median_income": 8.3252,
            "median_house_value": 452600.0,
            "ocean_proximity": "NEAR BAY",
        },
        {
            "longitude": -121.92,
            "latitude": 37.85,
            "housing_median_age": 35,
            "total_rooms": 1400,
            "total_bedrooms": 250,
            "population": 500,
            "households": 200,
            "median_income": 5.5,
            "median_house_value": 300000.0,
            "ocean_proximity": "INLAND",
        }
    ]

    for house in house_data:
        add_house(session, house)

    # 📜 Afficher les maisons stockées
    list_houses(session)

    # Fermer la session
    session.close()
