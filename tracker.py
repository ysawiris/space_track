from skyfield.api import Topos, load
from spack_track import getTLESatellites


station_url2 = getTLESatellites("2019-09-25--2019-09-26")


f = open("demofile4.txt", "w")
f.write(station_url2)
f.close()





ts = load.timescale()
t = ts.now()
bluffton = Topos('37.67 N', '122.08 W')
satellites = load.tle_file("demofile4.txt", reload=True)

print('Loaded', len(satellites), 'satellites') 
print(bluffton)

for satellite in satellites:
    geometry = satellite.at(t)
    subpoint = geometry.subpoint()
    latitude = subpoint.latitude
    longitude = subpoint.longitude
    elevation = subpoint.elevation
    difference = satellite - bluffton
    print(satellite)
    topocentric = difference.at(t)
    print(topocentric.position.km[2])
    # print("Latitude, Lng, Ele", latitude, longitude, elevation)






