from flask import Flask
import os
from main import app, asgi_app

API_KEY = os.getenv("GOOGLE-MAPS-KEY")