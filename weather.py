import urllib, json, sys, datetime

class weather():
	def __init__(self, location, temp, description, windDirection, windSpeed, date):
		self.location = location
		self.temp = "{0} C".format(str(round(temp, 1)))
		self.description = description
		self.windDirection = windDegToDirection(windDirection)
		self.windSpeed = "{0}mph".format(str(round(windSpeed, 1)))
		self.date = date

def windDegToDirection(deg):
	if deg >= 337.5 or deg < 22.5:
		return "N"
	elif deg>= 22.5 and deg < 67.5:
		return "NE"
	elif deg >= 67.5 and deg < 112.5:
		return "E"
	elif deg >= 112.5 and deg < 157.5:
		return "SE"
	elif deg >= 157.5 and deg < 202.5:
		return "S"
	elif deg >= 202.5 and deg < 247.5:
		return "SW"
	elif deg >= 247.5 and deg < 297.5:
		return "W"
	elif deg >= 297.5 and deg < 337.5:
		return "NW"

if __name__ == "__main__":
	arguments = sys.argv
	api = "http://maps.google.com/maps/api/geocode/json?address="
	APPID = "a3bd152386a24e0bd5529e158197c1b5"

	if len(arguments) < 2:
		# use ip address to get location
		ipAddr = json.loads(urllib.urlopen("http://ip-api.com/json").read())
		location = ipAddr["city"] + "+" + ipAddr["regionName"]
	else:
		# use arguments provided
		location = "+".join(arguments[1:])

	# get latlng coords from googles api
	api += location
	response = urllib.urlopen(api)
	data = json.loads(response.read())

	if data["status"] != "ZERO_RESULTS":
		lat = data["results"][0]["geometry"]["location"]["lat"]
		lng = data["results"][0]["geometry"]["location"]["lng"]

		weather_api = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&mode=json&appid={}&format=json".format(str(lat), str(lng), APPID)
		forecast_api = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&mode=json&appid={}&format=json".format(str(lat), str(lng), APPID)

		# hit open weather api to get todays weather
		response = urllib.urlopen(weather_api)
		data = json.loads(response.read())
		now = datetime.datetime.now()
		try:
			windDirecton = data["wind"]["deg"]
		except:
			windDirecton = "--mph"
		# hit open weather api to get weather forecast
		response = urllib.urlopen(forecast_api)
		today = weather(data["name"], data["main"]["temp"] - 273.15, data["weather"][0]["main"], windDirecton, data["wind"]["speed"] * 1.24, now)

		# hit open weather api to get weather forecast
		response = urllib.urlopen(forecast_api)
		data = json.loads(response.read())

		# Get the conditions at midday everyday from forecast api response
		forecasts = []
		for forecast in data["list"]:
		    if "12:00" in forecast["dt_txt"]:
				forecasts.append(forecast)

		# create day specific weather objects to store forecast data
		tomorrow = weather(today.location, forecasts[0]["main"]["temp"] - 273.15, forecasts[0]["weather"][0]["main"], forecasts[0]["wind"]["deg"], forecasts[0]["wind"]["speed"] * 1.24, now + datetime.timedelta(days=1))
		today_plus2 = weather(today.location, forecasts[1]["main"]["temp"] - 273.15, forecasts[1]["weather"][0]["main"], forecasts[1]["wind"]["deg"], forecasts[1]["wind"]["speed"] * 1.24, now + datetime.timedelta(days=2))
		today_plus3 = weather(today.location, forecasts[2]["main"]["temp"] - 273.15, forecasts[2]["weather"][0]["main"], forecasts[2]["wind"]["deg"], forecasts[2]["wind"]["speed"] * 1.24, now + datetime.timedelta(days=3))
		today_plus4 = weather(today.location, forecasts[3]["main"]["temp"] - 273.15, forecasts[3]["weather"][0]["main"], forecasts[3]["wind"]["deg"], forecasts[3]["wind"]["speed"] * 1.24, now + datetime.timedelta(days=4))

		# print forecast in a nice way
		print "\nWeather forecast for {}\n".format(today.location)

		print "{:<14}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format("", today.date.strftime("%a"), tomorrow.date.strftime("%a"), today_plus2.date.strftime("%a"), today_plus3.date.strftime("%a"), today_plus4.date.strftime("%a"))
		print "{:<14}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format("Conditions", today.description, tomorrow.description, today_plus2.description, today_plus3.description, today_plus4.description)
		print "{:<14}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format("Temp", today.temp, tomorrow.temp, today_plus2.temp, today_plus3.temp, today_plus4.temp)
		print "{:<14}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format("Wind Speed", today.windSpeed, tomorrow.windSpeed, today_plus2.windSpeed, today_plus3.windSpeed, today_plus4.windSpeed)
		print "{:<14}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format("Wind Direction", today.windDirection, tomorrow.windDirection, today_plus2.windDirection, today_plus3.windDirection, today_plus4.windDirection)
		print "\n",

	else:
		print "Couldn't find your location!"
