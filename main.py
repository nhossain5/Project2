"""
This is the main application file
"""
import os
from flask import Flask, render_template
from tmdb_and_wiki import get_movie_data

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=["POST", "GET"])
def hello_world():
    """
    This functions retrieves movie data and sends it to the index.html file
    """
    movie_data = get_movie_data()
    return render_template(
        "index.html",
        titles=movie_data['titles'],
        poster_paths=movie_data['poster_paths'],
        taglines=movie_data['taglines'],
        ids=movie_data['ids'],
        genres=movie_data['genres'],
        wikilinks=movie_data['wikilinks']
    )

app.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),
    debug=True
)
