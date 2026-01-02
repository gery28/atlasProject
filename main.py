from flask import Flask, render_template, render_template_string, Response, send_from_directory, url_for
from waitress import serve
import folium
from folium.plugins import FeatureGroupSubGroup, Search, MarkerCluster
import requests
import os
from tqdm import tqdm
import logging
from asgiref.wsgi import WsgiToAsgi

from build import titles_asia, markers_asia, titles_hun, markers_hun

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)
app.logger.setLevel(logging.DEBUG)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.DEBUG)

@app.route("/")
def fullscreen():
    # return m.get_root().render()
    #return Response(m.get_root().render(), mimetype="text/html")
    return render_template("map.html", title="Atlas")
    # return "asd"

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'static/favicon.ico', mimetype='image/vnd.microsoft.icon')

asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    # app.run(port=5000)
    serve(app, host="0.0.0.0", port=8080)
