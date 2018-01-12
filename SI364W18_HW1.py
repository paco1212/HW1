## HW 1
## SI 364 W18
## 1000 points

# Francisco "Paco" Gallardo
# SI 364 - Building Interactive Applications 
# Univesity of Michigan School of Information
#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

# None 

# ****** NOTE ******* #
# In order for you to run my program, you need to create and API key from accuweather
# The link to the website is: https://developer.accuweather.com/
# You need to create an account then on the right hand corner of the page, hover over your email
# Then click on "My Apps". Once you click on that, you need to create and app and fill out the form.
# Once you are done, then you need to create a python file called "accuweather.py" and 
# create a variable called apikey. Assign the variable apikey to be the string value of your api key that you created.
# After that, save the accuweather api file in the same directory that you have this file saved under.
# You are done and ready to run my project :)
# Have fun!

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
import json
import requests
from accuweather import apikey

app = Flask(__name__)
app.debug = True

# Default home page
@app.route('/')
def hello_to_you():
    return 'Hello World!'

# Problem 1
# Decorator function
@app.route('/class')
# When this link is accessed, call this function and display the return statement on the page
def class_364():
    return 'Welcome to SI 364!'



# Problem 2
# Decorator function
@app.route('/movie/<title>')
# When think link is accessed using a movie name,
# make a request to the iTunes API and 
# Display the results of the movie searched for on the page
def movie(title):
	baseurl = "https://itunes.apple.com/search" # iTunes API url
	data = requests.get(baseurl, params = {"term": title, "entity": "movie"}) # Making a requests to iTunes API
	text = (data.text) # Saving text from response object to new variable
	return text # Display the text from response object on the page
	

# Problem 3
# Decorator Function
@app.route('/question')
# When this link is accessed, display an HTML form that asks the user to submit their favorite number
def pregunta():
	s = """<!DOCTYPE html>
<html>
<body>
<form  action="/answer" method='POST'>
  What is your favorite number:<br>
  <input type="text" name="number" value=""> 
  <br>
  <input type="submit" value="Submit">
</form>
</body>
</html>"""
	return s

# Problem 3 continued
# When the user submits their favorite number to the previous page,
# Then attempt to cast the information submitted into a string. If it works, then multiple the number 
# by 2 and display it on the screen
# If I cannot cast the string as an integer, then display an error message on this new page
@app.route('/answer', methods = ['POST', 'GET'])
def respuesta():
	# To find out if the user submitted a number, try to cast it as a string and multiply it
	# If a number, then display a message and the new number
	try:
		text = request.form["number"]
		number = int(text)
		double = number * 2
		return "Double your favorite number is {}".format(double)
	# If not a number, display a message on the page that tells user that they did not submit a number
	except:
		return "You did not input a number"
	


# Problem 4
@app.route("/problem4form")
def form():
	# pass
	form = '''<!Documentation html>
	<html>
	<body>
	<form action="/problem4response" method="POST">
	<input type="text" name="search_query" value=""> Enter a city/town to get forecast:<br>

	<select name="Hours">
	<option value="1 Hour"> 1 Hour</option>
	<option value="12 Hours"> 12 Hours</option>



	<input type="submit" value="Submit">

	</form>
	</body>
	</html>'''
	return form

@app.route("/problem4response", methods = ["POST", "GET"])
def response():
	location_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
	city_query = request.form["search_query"]
	hour_selection = request.form["Hours"].split()
	hour_preference = int(hour_selection[0])
	try:
		location_data = requests.get(location_url, params = {"apikey": apikey, "q":city_query})
		obj = json.loads(location_data.text)
		city = str(obj[0]["Key"])
		state = str(obj[0]["AdministrativeArea"]["EnglishName"])
	except:
		return "Not a valid city"

	forecast_url = "http://dataservice.accuweather.com/forecasts/v1/hourly/"
	if hour_preference == 1:
		forecast_url += "/1hour/"
		forecast_url += city

		try:
			forecast_data = requests.get(forecast_url, params = {"apikey":apikey})
			forecast_obj = json.loads(forecast_data.text)
		
		except:
			return "Cannot display results for {},{}".format(city_query, state)

		degree = str(forecast_obj[0]["Temperature"]["Value"])
		unit = str(forecast_obj[0]["Temperature"]["Unit"])
		final = "The current weather of {},{} is: {}{}".format(city_query, state, degree,unit)

	elif hour_preference == 12:
		forecast_url += "/12hour/"
		forecast_url += city

		try:
			forecast_data = requests.get(forecast_url, params = {"apikey":apikey})
			forecast_obj = json.loads(forecast_data.text)
		
		except:
			return "Cannot display results for {},{}".format(city_query, state)

		temp_values = []
		for dic in forecast_obj:
			temp_values.append(dic["Temperature"]["Value"])
		final = "The current weather of {},{} is: {}F\n".format(city_query, state,temp_values[0])
		string = ""
		for i in range(1,12):
			string += "Temperature in {} hours: {}F\n".format(str(i), temp_values[i])
		final = final + string



	return (final)



if __name__ == '__main__':
    app.run()


## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.


## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.
