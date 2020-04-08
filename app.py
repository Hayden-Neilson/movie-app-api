from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" +os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column (db.String(120), nullable =False)
    year = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    starring = db.Column(db.String(100), nullable=False)

    def __init__(self, title, year, rating, genre, starring):
        self.title = title
        self.year = year
        self.rating = rating
        self.genre = genre
        self.starring = starring

class MovieSchema(ma.Schema):
    class Meta:
        fields = ("title", "year", "rating", "genre", "starring")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@app.route("/", methods= ["GET"])
def home():
    return "<h1>Movie app</h1>"


#Get
@app.route("/movieall", methods=["GET"])
def all_movies():
  all_movies = Movie.query.all()
  result = movies_schema.dump(all_movies)
  return jsonify(result)

# POST

@app.route('/share', methods = ["POST"])
def share_movie():
    title = request.json['title']
    year = request.json['year']
    rating = request.json['rating']
    genre = request.json['genre']
    starring = request.json['starring']

    new_movies = Movie("title", "year", "rating", "genre", "starring" )

    db.session.add(new_movies)
    db.session.commit()

    movies = Movie.query.get(new_movies.id)

    return movie_schema.jsonify(movies)



# PUT / PATCH
@app.route("/<id>", methods = ["PUT"])
def add_movies(id):
    movies = Movie.query.get(id)
    return movie_schema.jsonify(movies)


# DELETE

@app.route("/newlist/<id>", methods=["DELETE"])
def removing_movies(id):
    new_movies = Movie.query.get(id)
    db.session.delete(new_movies)
    db.session.commit()
    return movie_schema.jsonify(new_movies)




if __name__ == "__main__":
  app.debug = True
  app.run()