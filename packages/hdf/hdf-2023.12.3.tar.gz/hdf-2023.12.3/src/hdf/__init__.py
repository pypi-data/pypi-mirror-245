from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return "HDF 2023.12.0"
