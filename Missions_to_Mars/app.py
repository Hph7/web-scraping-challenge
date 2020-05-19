from flask import Flask, render_template, redirect
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
# Import your scrape_mars.py script
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
mongo = PyMongo(app)

# Create a root route / that will query your Mongo database and pass the mars data into 
# an HTML template to display the data.
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars=mars)

# create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.replace_one({}, mars_data, upsert = True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)