from flask import Flask

app = Flask(__name__)
app.secret_key = 'thisIsMySecretKey'
from my_app import views

