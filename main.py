# =======================================================================
# Project: Dog Photo Gallery
# Description: An interactive web application built with Python.
# Built with: Flask. The app retrieves data from a third-party REST API and uses Jinja to place the data in the app's HTML template.
# The app lets users:
# - see dog photos based on their selection of number of photos and dog breed from a drop down menu.
# - see a random dog photo on the click of a button. 
# Background: Coursework for Skillcrush's "Using Python to Build Web Apps" course.

# ==== *** ====

# The main.py file contains the code that manages the logic of/operates the app. It:
# - contains routing for retrieving the user's selection from HTML forms and for user requests for a random photo, handling error messages for the user, making API requests, and rendering data to the frontend.
# - converts JSON files to Python dictionaries.  
# =======================================================================

#Imports Flask, the render_template module, the request module (incl. the request object), and the requests library:
from flask import Flask, render_template, request
import requests
#imports a dictionary of data from dog_breeds.py and "prettifies", or styles, the dog names when they appear in the HTML page:
from dog_breeds import prettify_dog_breed

app = Flask("app")


#function adds a dash in the URL between breed names with multiple words like miniature poodle
def check_breed(breed):
    return "/".join(breed.split("-"))

# Retrieves user's selected number of photos and selected breed from API and returns/renders result to the frontend: 
@app.route("/", methods=["GET", "POST"])  #Adds GET and POST methods.
def dog_image_gallery():
    #List holds error messages:
    errors = []
    #The request object checks if the request method is POST or not:
    if request.method == "POST":
        #The request object gets the key/value pairs from the html <form> (string equals names in drop-down menu) containing the POST method, and saves the retrieved data in the breed variable:
        breed = request.form.get("breed")
        #The request object gets the number of images selected by user:
        number = request.form.get("number")
        #Checks if user selected a breed from menu or not:
        if not breed:
            errors.append("Oops! Please choose a dog breed.")
        #Checks if user did not select a number from menu:
        if not number:
          errors.append("Oops! Please choose a number.")
        #Calls API if user selected a breed and a number from the menu:
        if breed and number:
            response = requests.get("https://dog.ceo/api/breed/" +
                                    check_breed(breed) + "/images/random/" + number)
            #Converts JSON file to Py dictionary and stores data from file:
            data = response.json()
            #Holds the dictionary and assigns "message" key to access desired data in the JSON file that is stored in the dictionary:
            dog_images = data["message"]
            # Sends dictionary data to the html template: 
            return render_template("dogs.html", images=dog_images, breed=prettify_dog_breed(breed), errors=[])
    # Handles html template rendering when no menu selection has been made and displays the heading, menu, submit button, and the error msg.:      
    return render_template("dogs.html", images=[], breed="", errors=errors)

# Retrieves a random dog photo from API and returns/renders to frontend:
@app.route("/random", methods=["POST"])
def get_random():
  # Calls API:
  response = requests.get("https://dog.ceo/api/breeds/image/random")
  # Converts JSON file to Py dictionary and stores the extracted data from the JSON file:
  data = response.json()
  #Holds the dictionary and assigns "message" key to access desired data in the JSON file that is stored in the dictionary:
  dog_images = [data["message"]] 
  # Sends dictionary data to the html template:
  return render_template("dogs.html", images=dog_images)

app.debug = True
app.run(host='0.0.0.0', port=8080)
