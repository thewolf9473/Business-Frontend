from email.mime import text
import emails
import random
import string
from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from mail_generator import generate_mail

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/success', methods=["POST", "GET"])
def success():
    if request.method == "POST":
        return render_template('home.html')


@app.route('/minutes', methods=["POST", "GET"])
def result():
    if request.method == "POST":

        message = emails.html(
            html="<h1>This is an email</h1><strong>We love sending emails</strong>",
            subject="Hey, look in here!",
            mail_from="deepconteam@gmail.com",
        )
        # sender = "deepconteam@gmail.com"
        receivers = request.form.get("email")
        file = request.form.get("file")
        # receivers_name = request.form.get("name")

        # subject, text = generate_mail(receivers_name)
        # message = MIMEText(text)

        # message['Subject'] = subject
        # message['From'] = sender
        # message['To'] = receivers

        # server = smtplib.SMTP(
        #     "email-smtp.ap-south-1.amazonaws.com", 587)
        # server.starttls()
        # server.login(sender, "BFuujoxH6uJA3RYSZDIUDII3XTxJr4ReQweABpINju70")
        # server.sendmail(sender, receivers, message.as_string())

        r = message.send(
            to=receivers,
            smtp={
                "host": "email-smtp.ap-south-1.amazonaws.com",
                "port": 587,
                "timeout": 5,
                "user": "AKIA4QB2WTN5WRHMWS4U",
                "password": "BFuujoxH6uJA3RYSZDIUDII3XTxJr4ReQweABpINju70",
                "tls": True,
            }
        )

        print(r.status_code)
        print(file)
        return render_template('result.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
