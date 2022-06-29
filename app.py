from concurrent.futures import process
import emails
import random
import string
from flask import Flask, render_template, request, redirect
import requests
from mail_generator import send_email
from utilities import upload_to_aws
import os
import asyncio
import time
import httpx
from dotenv import load_dotenv
from database_handler import insert_values, get_result, authenticate_login
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)
load_dotenv()


app = Flask(__name__)

app.config["MP3_UPLOADS"] = "static/images/uploads"


def generate_process_code():
    x = ''.join(random.choice(string.ascii_uppercase +
                string.ascii_lowercase + string.digits) for _ in range(4))
    return x


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/success', methods=["POST", "GET"])
def success():
    template = 'nologin.html'
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print("email: ", email)
        print("password: ", password)
        auth = authenticate_login(email, password)
        print('auth:', auth)
        if auth:
            template = 'home.html'
    return render_template(template)


@app.route('/minutes', methods=["POST", "GET"])
async def result():
    if request.method == "POST":

        sender = "deepconteam@gmail.com"
        receivers = request.form.get("email")
        file = request.files["audio"]
        translation = ' '.join(request.form.getlist('Translation'))
        length = request.form.get('length')
        num_speakers = request.form.get('num-speakers')
        print('length', length)
        print('translation checkbox ', translation)
        frontend_start_time = time.time()
        file.save(os.path.join(app.config["MP3_UPLOADS"], file.filename))
        file_path = "static/images/uploads/{}".format(file.filename)
        print("-------------file path -------------- ", file_path)
        receivers_name = request.form.get("name")
        process_code = generate_process_code()
        res = upload_to_aws(file_path, file_name=process_code)
        

        try:

            async with httpx.AsyncClient() as client:
                params_dict = {'process_code': process_code,
                               'receiver_email': receivers,
                               'receiver_name': receivers_name,
                               'translation': translation,
                               'length': length,
                               'num_speakers': num_speakers,
                               'frontend_start_time':frontend_start_time
                               }
                res = await asyncio.gather(
                    client.post('http://server-service.default.svc.cluster.local:8000/getcode',
                                params=params_dict)
                )
                
                print("---------------------------------------------------------API-Working--------------------------------------------------------------")

        except:
            print("microservice request not processed")

        insert_values(process_code=process_code,
                      receiver_name=receivers_name,
                      receiver_email=receivers,
                      )

        email_res = send_email(process_code=process_code,
                               receiver_email=receivers,
                               receivers_name=receivers_name,
                               sender=sender)

        return render_template('greetings.html')


@app.route('/get-transcript')
def sample():
    return render_template('result.html')


@app.route('/get-transcript', methods=["POST", "GET"])
def my_form_post():
    if request.method == 'POST':
        process_code = request.form.get('Process_code')
        ziped_list, process_code, user_name = get_result(process_code)
    return render_template('result.html', list=ziped_list, process_code=process_code, user_name=user_name)


# @app.route('/get-transcript', methods=["POST", "GET"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
