import ephem

sun = ephem.Sun()
city = ephem.Observer()
city.lon, city.lat = '40.7608', '111.8910'
sun.compute(city)
night = -12 * ephem.degree

if sun.alt < night:
    print("It's dark yo! Let me turn the lights on for you")

if sun.alt > night:
    print("It's bright yo")

