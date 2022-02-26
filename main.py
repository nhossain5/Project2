"""
This is the main application file
"""
import os
import flask
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from tmdb_and_wiki import get_movie_data

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieID = db.Column(db.Integer)
    comment = db.Column(db.String(128))
    rating = db.Column(db.Integer)


db.create_all()


@app.route("/", methods=["POST", "GET"])
def hello_world():
    """
    This functions retrieves movie data and sends it to the index.html file
    """
    movie_data = get_movie_data()
    reviews = Reviews.query.filter_by(movieID=movie_data["ids"][0]).all()
    num_reviews = len(reviews)

    return render_template(
        "index.html",
        titles=movie_data["titles"],
        poster_paths=movie_data["poster_paths"],
        taglines=movie_data["taglines"],
        ids=movie_data["ids"],
        genres=movie_data["genres"],
        wikilinks=movie_data["wikilinks"],
        reviews=reviews,
        num_reviews=num_reviews,
    )


@app.route("/review_added", methods=["GET", "POST"])
def review_added():
    if flask.request.method == "POST":
        data = flask.request.form
        new_review = Reviews(
            movieID=data["movieID"], comment=data["comment"], rating=data["rating"]
        )
        if (
            Reviews.query.filter_by(
                movieID=new_review.movieID,
                comment=new_review.comment,
                rating=new_review.rating,
            ).first()
        ) is None:
            db.session.add(new_review)
            db.session.commit()
        else:
            return flask.redirect("/")

    movie_data = get_movie_data()
    reviews = Reviews.query.filter_by(movieID=movie_data["ids"][0]).all()
    num_reviews = len(reviews)
    return flask.render_template(
        "index.html",
        reviews=reviews,
        num_reviews=num_reviews,
        titles=movie_data["titles"],
        poster_paths=movie_data["poster_paths"],
        taglines=movie_data["taglines"],
        ids=movie_data["ids"],
        genres=movie_data["genres"],
        wikilinks=movie_data["wikilinks"],
    )


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
