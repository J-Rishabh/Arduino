from flask import Flask, render_template, request, redirect, url_for
from jinja2 import Template
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_body, solar_system_ephemeris, get_moon, get_body_barycentric
from datetime import datetime
from geopy.geocoders import Nominatim
from time import sleep
import json
import requests
from pycraf import satellite
from serialcontrol import returnMotor, moveMotor


app = Flask(__name__)
dataArray = []

# getting location and changing it into latitude/longitude with geopy
@app.template_global()
def coordinateFinder(location, curTime, userObject):
    returnData = []
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(location, timeout=10)
    locationElevation = 10


    #print(getLoc.address)
    #print("Latitude = ", getLoc.latitude, "\n")
    #print("Longitude = ", getLoc.longitude)
    returnData.append(getLoc.latitude)
    returnData.append(getLoc.longitude)
    returnData.append(getLoc.address)



    currentLocation = EarthLocation(lat=(getLoc.latitude)*u.deg, lon=getLoc.longitude*u.deg, height=locationElevation*u.m)
    utcoffset = -4*u.hour  # Eastern Daylight Time

    currentTime = datetime.now()

    time = Time(currentTime) - utcoffset
    #print(currentTime)
    #print(time)

    returnData.append(currentTime)


    # for messier objects
    try:
        userObj = SkyCoord.from_name(userObject)
    except:
        return coordinateFinderSolarSystem(location, currentTime, userObject)
    else:
        userObjaltaz = userObj.transform_to(AltAz(obstime=time,location=currentLocation))

        returnData.append(userObject.title())

        #print(userObjaltaz)
        #print("ALT: " + str(userObjaltaz.alt.degree))
        #print("AZ: " + str(userObjaltaz.az.degree))

        returnData.append(round(userObjaltaz.alt.degree,3))
        returnData.append(round(userObjaltaz.az.degree, 3))

        # can also do .radian for radians!
        # returns the following
        # user latitude, user longitude, fullAddress, time, object, altitude, azimuth
        print(returnData)
        return returnData


    '''userObj = SkyCoord.from_name(userObject)

    userObjaltaz = userObj.transform_to(AltAz(obstime=time,location=currentLocation))

    returnData.append(userObject)

    #print(userObjaltaz)
    print("ALT: " + str(userObjaltaz.alt.degree))
    print("AZ: " + str(userObjaltaz.az.degree))

    returnData.append(userObjaltaz.alt.degree)
    returnData.append(userObjaltaz.az.degree)

    # can also do .radian for radians!

    altitude = userObjaltaz.alt.degree
    azimuth = userObjaltaz.az.degree
    # returns the following
    # user latitude, user longitude, fullAddress, time, object, altitude, azimuth
    return returnData'''

def coordinateFinderSolarSystem(location, curTime, userObject):
    if "moon" in userObject.lower():
        return coordinateFinderMoon(location, curTime)
    elif "iss" in userObject.lower() or "international space station" in userObject.lower():
        return coordinateFinderISS(location, curTime)
    else:

        returnData = []
        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(location, timeout=10)
        locationElevation = 10


        #print(getLoc.address)
        #print("Latitude = ", getLoc.latitude, "\n")
        #print("Longitude = ", getLoc.longitude)
        returnData.append(getLoc.latitude)
        returnData.append(getLoc.longitude)
        returnData.append(getLoc.address)



        currentLocation = EarthLocation(lat=(getLoc.latitude)*u.deg, lon=getLoc.longitude*u.deg, height=locationElevation*u.m)
        utcoffset = -4*u.hour  # Eastern Daylight Time

        currentTime = datetime.now()

        time = Time(currentTime) - utcoffset
        #print(currentTime)
        #print(time)

        returnData.append(currentTime)

        
        try:
            with solar_system_ephemeris.set('builtin'):
                planetData = get_body(userObject, Time(currentTime))
                
        except:
            #coordinateFinderSolarSystem(location, curTime, userObject)
            print("AAAAA1")
        else:

            #print(planetData)

            userObjaltaz = planetData.transform_to(AltAz(obstime=time,location=currentLocation))

            returnData.append(userObject.title())

            #print(userObjaltaz)
            #print("ALT: " + str(userObjaltaz.alt.degree))
            #print("AZ: " + str(userObjaltaz.az.degree))

            returnData.append(round(userObjaltaz.alt.degree, 3))
            returnData.append(round(userObjaltaz.az.degree, 3))

            # can also do .radian for radians!
            # returns the following
            # user latitude, user longitude, fullAddress, time, object, altitude, azimuth
            print(returnData)
            return returnData

def coordinateFinderMoon(location, curTime):
    returnData = []
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(location, timeout=10)
    locationElevation = 10


    #print(getLoc.address)
    #print("Latitude = ", getLoc.latitude, "\n")
    #print("Longitude = ", getLoc.longitude)
    returnData.append(getLoc.latitude)
    returnData.append(getLoc.longitude)
    returnData.append(getLoc.address)



    currentLocation = EarthLocation(lat=(getLoc.latitude)*u.deg, lon=getLoc.longitude*u.deg, height=locationElevation*u.m)
    utcoffset = -4*u.hour  # Eastern Daylight Time

    currentTime = datetime.now()

    time = Time(currentTime) - utcoffset
    #print(currentTime)
    #print(time)

    returnData.append(currentTime)


    
    with solar_system_ephemeris.set('builtin'):
        Data = get_moon(time, currentLocation)

    #coordinateFinderSolarSystem(location, curTime, userObject)
    #print("AAAAA")



    userObjaltaz = Data.transform_to(AltAz(obstime=time,location=currentLocation))

    returnData.append("Moon")

    #print(userObjaltaz)
    
    #print(Data.lon)
    #print("ALT: " + str(userObjaltaz.alt.degree))
    #print("AZ: " + str(userObjaltaz.az.degree))

    returnData.append(round(userObjaltaz.alt.degree, 3))
    returnData.append(round(userObjaltaz.az.degree, 3))

    # can also do .radian for radians!

    altitude = userObjaltaz.alt.degree
    azimuth = userObjaltaz.az.degree
    # returns the following
    # user latitude, user longitude, fullAddress, time, object, altitude, azimuth
    print(returnData)
    return returnData

#coordinateFinderMoon("NYC", 4)
def coordinateFinderISS(location, curTime):
    returnData = []
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(location, timeout=10)
    locationElevation = 10


    #print(getLoc.address)
    #print("Latitude = ", getLoc.latitude, "\n")
    #print("Longitude = ", getLoc.longitude)
    returnData.append(getLoc.latitude)
    returnData.append(getLoc.longitude)
    returnData.append(getLoc.address)



    currentLocation = EarthLocation(lat=(getLoc.latitude)*u.deg, lon=getLoc.longitude*u.deg, height=locationElevation*u.m)
    utcoffset = -4*u.hour  # Eastern Daylight Time

    currentTime = datetime.now()

    time = Time(currentTime) - utcoffset
    #print(currentTime)
    #print(time)

    returnData.append(currentTime)

    returnData.append("International Space Station")
    #TLEdata = json.loads(requests.get("https://tle.ivanstanojevic.me/api/tle/25544").text)
    #print(TLEdata)
    #TLEname = TLEdata['name']
    #TLEline1 = TLEdata['line1']
    #TLEline2 = TLEdata['line2']

    TLEdata = (requests.get("https://live.ariss.org/iss.txt").text).splitlines()
    #print(TLEdata)
    TLEname = TLEdata[0]
    TLEline1 = TLEdata[1]
    TLEline2 = TLEdata[2]
    dataString = TLEname + "\n" + TLEline1 + "\n" + TLEline2

    #print(dataString)
    sat_obs = satellite.SatelliteObserver(currentLocation)

    az, el, dist = sat_obs.azel_from_sat(dataString, time)
    #print('az, el, dist: {:.1f}, {:.1f}, {:.0f}'.format(az, el, dist)) 

    returnData.append(round(float(el.value), 3))
    returnData.append(round(float(az.value), 3))

    # returns the following
    # user latitude, user longitude, fullAddress, time, object, altitude, azimuth
    print(returnData)
    return returnData

#coordinateFinder("NYC", 4, "ISS")
@app.route('/stopTracking')
def stopTracking():
    returnMotor()
    print("WOOO!")
    return ("nothing")

def scaleMotor(num):
    num = num / 360 
    num = round(num * 200) % 200
    if (num > 100):
        return -(200-num)
    else:
        return num

app.jinja_env.globals.update(coordinateFinder=coordinateFinder)

oldalt = 0
oldaz = 0
myaltlist = [0]
myazlist = [0]
@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
    #dataArray = coordinateFinder("NYC", 4, "M31")
    # home page, allows user to input location
        loc = str(request.form["nm"])
        tm = 1
        obj = str(request.form["nm2"])
        #print(loc)
        #print(url_for("calculate", location=loc))
        
        dataArray = coordinateFinder(loc, 4, obj)
        myalt = scaleMotor(dataArray[5])
        myaz = scaleMotor(dataArray[6])
        myaltlist.append(myalt)
        myazlist.append(myaz)
        oldalt = myaltlist[len(myaltlist)-2]
        oldaz = myazlist[len(myazlist)-2]

        print("OLDALT: " + str(oldalt) + " NEW: " + str(myalt))
        print("OLDALT: " + str(oldaz) + " NEW: " + str(myaz))
        tmpalt = myalt - oldalt
        tmpaz = myaz - oldaz
        moveMotor(tmpalt, tmpaz)
        #print("AAAA")
        # user latitude, user longitude, fullAddress, time, object, altitude, azimuth
        return  render_template("results.html", latitude = dataArray[0], longitude =dataArray[1], fullAddress = dataArray[2], time = dataArray[3], object = dataArray[4], altitude = dataArray[5], azimuth = dataArray[6])
        #return redirect(url_for("calculate", location=loc, time = tm, object = obj))
    else:

        return render_template('index.html')

# ?location=

'''
# parameters - location = , time = 
@app.route('/results/<location>')
def calculate(location, time, object):
   # results page, allows user to navigate back also
   #dataArray = coordinateFinder("NYC", 4, "M31")
   return f"<h1>{location}</h1>"
   #return render_template('results.html')
'''
if __name__ == '__main__':
   #app.debug = True
   #coordinateFinder("NYC", 4, "M31")
   app.run(debug=True)

 
