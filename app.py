# use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for

# use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo

# to use the scraping code, we will use the file converted from Jupyter notebook to Python
import scraping

# set up Flask
app = Flask(__name__)

# tell Python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page when we're looking at the home page
@app.route("/")
def index():
   # uses PyMongo to find the "mars" collection in our database
   mars = mongo.db.mars.find_one()
   # tells Flask to return an HTML template using an index.html file
   return render_template("index.html", mars=mars)

# This route, “/scrape”, will run the function that we create just beneath it.
@app.route("/scrape")
def scrape():
   # assign a new variable that points to our Mongo database
   mars = mongo.db.mars
   # new variable to hold the newly scraped data
   # referencing the scrape_all function in the scraping.py file imported
   mars_data = scraping.scrape_all()
   # Now that we've gathered new data, we need to update the database 
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()