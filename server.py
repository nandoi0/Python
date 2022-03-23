from flask import Flask

app = Flask("Server")

@app.route("/")
def home():
    return "Hello from Flask"


@app.route("/me")
def about_me():
    return "Fernando Iribe"

app.run(debug=True)