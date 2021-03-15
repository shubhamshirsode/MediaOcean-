import requests
import json
from flask import Flask
from flask import (
    request, Blueprint, Response
)
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@123@localhost/mediaoceandb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MovieInTheatres(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), index=False, unique=False, nullable=False)
   release_year = db.Column(db.Integer, index=False, unique=False, nullable=False)
   genres = db.Column(db.String(200), index=False, unique=False, nullable=False)
   description = db.Column(db.Text, index=False, unique=False, nullable=False)
   theatre = db.Column(db.String(200), index=False, unique=False, nullable=False)


class MovieInTV(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(200), index=False, unique=False, nullable=False)
   release_year = db.Column(db.Integer, index=False, unique=False, nullable=False)
   genres = db.Column(db.String(200), index=False, unique=False, nullable=False)
   description = db.Column(db.Text, index=False, unique=False, nullable=False)
   channel = db.Column(db.String(200), index=False, unique=False, nullable=False)



@app.route('/get_local_movie_data',methods = ['POST', 'GET'])
def get_local_theatres_movie_data():
   try:
      if request.method == 'GET':
         # import pdb;pdb.set_trace()
         start_date = request.args.get('start_date')
         zip_code = request.args.get('zip_code')
         api_secret = request.args.get('api_secret')
         response = requests.request("GET", f'http://data.tmsapi.com/v1.1/movies/showings?startDate={start_date}&zip={zip_code}&api_key={api_secret}')

         for obj in json.loads(response.text):
            new_record = MovieInTheatres(
               title=obj['title'],
               release_year=obj['releaseYear'] if 'releaseYear' in obj else 0,
               genres=str(obj['genres']) if 'releaseYear' in obj else '',
               description=obj['longDescription'] if 'longDescription' in obj else '',
               theatre=obj['showtimes'][0]['theatre']['name']
            )
            db.session.add(new_record)  # Adds new record to database
            db.session.commit()  # Commits all changes
      return Response(json.dumps({'status':True}), mimetype='application/json')

   except Exception as e:
      return Response(json.dumps({'status': False}), mimetype='application/json')

@app.route('/get_tv_movie_data',methods = ['POST', 'GET'])
def get_tv_movie_data():
   try:
      if request.method == 'GET':
         import pdb;
         pdb.set_trace()
         date_time = request.args.get('date_time')
         line_up_id = request.args.get('line_up_id')
         api_secret = request.args.get('api_secret')
         response = requests.request("GET", f'http://data.tmsapi.com/v1.1/movies/airings?lineupId={line_up_id} &startDateTime={date_time}&api_key={api_secret}')


         print('>>>>>>>>>>>',response.text)

         for obj in json.loads(response.text):
            new_record = MovieInTV(
               title=obj['title'],
               release_year=obj['releaseYear'] if 'releaseYear' in obj else 0,
               genres=str(obj['genres']) if 'releaseYear' in obj else '',
               description=obj['longDescription'] if 'longDescription' in obj else '',
               channel=obj['showtimes'][0]['theatre']['name']
            )
            db.session.add(new_record)  # Adds new record to database
            db.session.commit()  # Commits all changes
         return Response(json.dumps({'status':True}), mimetype='application/json')

   except Exception as e:
      return Response(json.dumps({'status': False}), mimetype='application/json')

if __name__ == '__main__':
    app.run()
