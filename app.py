from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/success', methods=["POST","GET"])
def success():
    if request.method == "POST":
        message = request.form
        print(message["email"])
        return f"{message} from login app."

if __name__ == 'main':
   app.run(debug = True)