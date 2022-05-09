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


def generate_result(transcript_link, minute_link, translated_output, languages, user_name="user", process_code=""):

    # process_code = generate_process_code()
    translated_str = "  "
    for i in range(len(languages)):
        lan = languages[i]
        trans = translated_output[i]
        translated_str = translated_str + '\n' + \
            f"* Translated {lan} minutes: {trans}"
    TEXT = f"""Hello {user_name}, We're glad that you've chosen DeepCon. your processing of request is completed and you can download files here. Please find the information below: \n
    * Your Request Number: {process_code}\n
    * Transcript Link: {transcript_link}\n
    * Minutes Link: {minute_link}\n   {translated_str}"""

    path_to_file = f"static/result/{process_code}.txt"
    with open(path_to_file, "w") as text_file:
        text_file.write(TEXT)

    return path_to_file


def get_result(process_code: str):

    client = MongoClient(
        "mongodb+srv://Majorcms:Majorcms@khoj.nqwbp.mongodb.net/khoj?retryWrites=true&w=majority")
    db = client.MajorCMS
    collection = db.MajorCMS

    myquery = {"process_code": process_code}
    mydoc = collection.find(myquery)
    translated_output = []
    for x in mydoc:
        transcript_link = x["processed_transcript_link"]
        minute_link = x['processed_minutes_link']
        languages = x['languages'].split()
        print(languages)
        print(type(languages))
        for j in languages:
            print(j)
            translated_output.append(
                x[f'processed_{j}_translated_minutes_link'])
        text = generate_result(transcript_link=transcript_link,
                               minute_link=minute_link,
                               translated_output=translated_output,
                               languages=languages,
                               process_code=process_code)

    return text


def authenticate_login(email, password):
    client = MongoClient(
        "mongodb+srv://Majorcms:Majorcms@khoj.nqwbp.mongodb.net/khoj?retryWrites=true&w=majority")
    db = client.MajorCMS
    collection = db.Login
    myquery = {"email": email}
    mydoc = collection.find(myquery)
    for x in mydoc:
        true_pass = x["password"]
        print('true pass: ', true_pass)
        if password == true_pass:
            print('authentication successfull')
            return True
        else:
            print('authentication not successfull')
            return False
