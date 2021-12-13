from email.mime import text
import random, string
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
        
        sender = "nidbhavsar989@gmail.com"
        receivers = request.form.get("email")
        receivers_name = request.form.get("name")

        subject, text = generate_mail(receivers_name)
        message = MIMEText(text)

        message['Subject'] = subject
        message['From'] = sender
        message['To'] = receivers

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, "15004959@Nb")
        server.sendmail(sender, receivers, message.as_string())

        return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
