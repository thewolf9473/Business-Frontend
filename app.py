import emails
import random
import string
from flask import Flask, render_template, request, redirect
import requests
from mail_generator import generate_mail
from utilities import upload_to_aws
import os
import asyncio, httpx
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_USER_PASSWORD = os.getenv("EMAIL_USER_PASSWORD")


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

        subject, text = generate_mail(receivers_name, process_code)
        res = upload_to_aws(file_path, file_name=process_code )
        print(res)
       

        message = emails.html(
            text=text,
            subject=subject,
            mail_from=sender,
        )
        
        try:
        
            # req = requests.post('http://server-service.default.svc.cluster.local:8000/getcode',
            #                 params={'process_code': process_code})
            
            async with httpx.AsyncClient() as client:
                params_dict = {'process_code': process_code, 
                               'receiver_email': receivers,
                               'receiver_name': receivers_name
                               }
                print(params_dict)
                res = await asyncio.gather(
                    client.post('http://localhost:8000/getcode', params= params_dict)
                    # client.post('http://server-service.default.svc.cluster.local:8000/getcode', params={'process_code': process_code})
                )
                # req = requests.post()
        except:
            print("microservice request not processed")
     

        r = message.send(
            to=receivers,
            smtp={
                "host": "email-smtp.ap-south-1.amazonaws.com",
                "port": 587,
                "timeout": 5,
                "user": EMAIL_USER,
                "password": EMAIL_USER_PASSWORD,
                "tls": True,
            }
        )

        return render_template('result.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
