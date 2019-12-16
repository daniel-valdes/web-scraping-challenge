from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create connection variable
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)


@app.route('/')
def index():

    mars = mongo.db.collection.find_one()

    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():

    mars = mongo.db.collection
    mars_data = scrape_mars.scrape()

    mars.update({}, mars_data, upsert=True)
    
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)