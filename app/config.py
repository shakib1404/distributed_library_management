import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://she:1234@cluster0.dtuaa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "demofast")
