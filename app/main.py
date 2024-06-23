from fastapi import FastAPI
from app.routes import user, link, join
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017")
db = client['mydatabase']

# Insert initial data to create the database if not already created
def create_initial_data():
    if db.users.count_documents({}) == 0:
        db.users.insert_one({"username": "initial_user", "email": "initial@example.com", "password": "password"})
        print("Initial data inserted to create the database")

create_initial_data()

app.include_router(user.router, prefix="/user")
app.include_router(link.router, prefix="/link")
app.include_router(join.router, prefix="/data")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


