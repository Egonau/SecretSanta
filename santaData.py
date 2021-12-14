from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Egonau:egoregoregor@vacancy.ggsch.mongodb.net/lycjobdata?retryWrites"
                      "=true&w=majority")
db = cluster["SecretSanta"]
users = db["Users"]
