import emails
import random
import string
from flask import Flask, render_template, request, redirect
import requests
from mail_generator import send_email
from utilities import upload_to_aws
import os
import asyncio, httpx
from dotenv import load_dotenv
from database_handler import insert_values
load_dotenv()


app = Flask(__name__)

app.config["MP3_UPLOADS"] = "static/images/uploads"
def generate_process_code():
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    return x

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/success', methods=["POST", "GET"])
def success():
    if request.method == "POST":
        return render_template('home.html')


@app.route('/minutes', methods=["POST", "GET"])
async def result():
    if request.method == "POST":
        
        sender = "deepconteam@gmail.com"
        receivers = request.form.get("email")
        file = request.files["audio"]
        file.save(os.path.join(app.config["MP3_UPLOADS"], file.filename))
        file_path = "static/images/uploads/{}".format(file.filename)
        print("-------------file path -------------- ", file_path)
        
            
        receivers_name = request.form.get("name")
        process_code = generate_process_code()
        res = upload_to_aws(file_path, file_name=process_code )
                
        try:
            
            async with httpx.AsyncClient() as client:
                    params_dict = {'process_code': process_code, 
                                'receiver_email': receivers,
                                'receiver_name': receivers_name
                                }
                    res = await asyncio.gather(
                            client.post('http://localhost:8000/getcode', params= params_dict)
                    )
                    
        except:
            print("microservice request not processed")
            
        insert_values(process_code= process_code,
                      receiver_name= receivers_name,
                      receiver_email= receivers,
                      )
        
        email_res = send_email(process_code=process_code, 
                                   receiver_email= receivers, 
                                   receivers_name= receivers_name,
                                   sender= sender)

        return render_template('result.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
