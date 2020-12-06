#Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_marsdata

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Create Flask Routes
#Root
@app.route("/")
def index():
    listings = mongo.db.mars.find_one()
    return render_template("index.html", listings=listings)

#Scraping Route
@app.route("/scrape")
def scraper():
    listings = mongo.db.mars
    listings_data = scrape_marsdata.scrape()
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
