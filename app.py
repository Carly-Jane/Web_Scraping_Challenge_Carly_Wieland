import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_info = scrape_mars.scrape_info()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_info, upsert=True)
    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)