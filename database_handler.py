from pymongo import MongoClient


def insert_values(receiver_name: str, receiver_email: str, process_code: str):
    
    status = False
    try:
        conn = MongoClient()
        status = True
        print("Connected successfully!!!")
    except:
        status = False  
        print("Could not connect to MongoDB")
        
    client = MongoClient("mongodb+srv://Majorcms:Majorcms@khoj.nqwbp.mongodb.net/khoj?retryWrites=true&w=majority")
    db = client.MajorCMS
    
    emp_rec1 = {
        "name": receiver_name,
        "process_code": process_code,
        "email": receiver_email
        }
    
    collection = db.MajorCMS
    res = collection.insert_one(emp_rec1)
    
    return status