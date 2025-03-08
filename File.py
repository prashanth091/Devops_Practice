from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Nagarajan! Welcome to your simple web application."

if __name__ == "__main__":
    app.run(debug=True)
 