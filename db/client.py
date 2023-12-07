
# Levantar server de MongoDB en local: 
#       ./mongod --dbpath "/home/jean/Documents/backend/MongoDB/data/"
#   Nota: Se debe posicionar en el path: /home/jean/Documents/backend/MongoDB/bin

from pymongo import MongoClient

dbClient = MongoClient().local



