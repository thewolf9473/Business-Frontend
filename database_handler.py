from matplotlib import use
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

    client = MongoClient(
        "mongodb+srv://Majorcms:Majorcms@khoj.nqwbp.mongodb.net/khoj?retryWrites=true&w=majority")
    db = client.MajorCMS

    emp_rec1 = {
        "name": receiver_name,
        "process_code": process_code,
        "email": receiver_email
    }

    collection = db.MajorCMS
    res = collection.insert_one(emp_rec1)

    return status


def generate_result(transcript_link, minute_link, keyword_link, translated_output, keyword_translated_output, transcripts_translated_output, languages, user_name="user", process_code=""):

    names_list = []
    link_list = []
    name_dict = {"fr": "French",
                 "de": "German",
                 "ru": "Russian",
                 "hi": "Hindi",
                 "it": "Italian"}
    names_list.extend(
        ['English Transcripts', 'English Minutes', 'English Keywords'])
    link_list.extend([transcript_link, minute_link, keyword_link])
    # process_code = generate_process_code()
    translated_str = "  "
    
    for lang, output in zip(languages, transcripts_translated_output):
        lang_ = name_dict[lang]
        names_list.append(f'{lang_} Transcripts')
        link_list.append(output)
    
    for lang, output in zip(languages, translated_output):
        lang_ = name_dict[lang]
        names_list.append(f'{lang_} Minutes')
        link_list.append(output)

    for lang, output in zip(languages, keyword_translated_output):
        lang_ = name_dict[lang]
        names_list.append(f'{lang_} Keywords')
        link_list.append(output)

    return list(zip(names_list, link_list))


def get_result(process_code: str):

    client = MongoClient(
        "mongodb+srv://Majorcms:Majorcms@khoj.nqwbp.mongodb.net/khoj?retryWrites=true&w=majority")
    db = client.MajorCMS
    collection = db.MajorCMS

    myquery = {"process_code": process_code}
    mydoc = collection.find(myquery)
    transcript_output = []
    translated_output = []
    keyword_output = []
    for x in mydoc:
        transcript_link = x["processed_transcript_link"]
        minute_link = x['processed_minutes_link']
        keyword_link = x['processed_keywords_link']
        user_name = x['name']
        languages = x['languages'].split()
        print(languages)
        print(type(languages))
        for j in languages:
            print(j)
            translated_output.append(
                x[f'processed_{j}_translated_minutes_link'])
            keyword_output.append(
                x[f'processed_{j}_translated_keywords'])
            transcript_output.append(
                x[f'processed_{j}_translated_transcripts'])
        zip_list = generate_result(transcript_link=transcript_link,
                                   minute_link=minute_link,
                                   keyword_link=keyword_link,
                                   translated_output=translated_output,
                                   languages=languages,
                                   process_code=process_code,
                                   keyword_translated_output=keyword_output,
                                   transcripts_translated_output = transcript_output,
                                   user_name=user_name)
    code = f'Process code: {process_code}'
    name = f'User Name: {user_name}'
    return zip_list, code, name


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
