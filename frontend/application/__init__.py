from flask import Flask, request
import os

app = Flask(__name__)

from application import routes