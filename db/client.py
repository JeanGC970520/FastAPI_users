
# Levantar server de MongoDB en local: 
#       ./mongod --dbpath "/home/jean/Documents/backend/MongoDB/data/"
#   Nota: Se debe posicionar en el path: /home/jean/Documents/backend/MongoDB/bin

from pymongo import MongoClient

# Conexion a la DB local
#dbClient = MongoClient().local

# Conexion a la DB remota
dbClient = MongoClient("mongodb+srv://test:test@cluster0.qdkdt1w.mongodb.net/?retryWrites=true&w=majority").test



