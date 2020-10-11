import serial, sys
ser = serial.Serial('/dev/ttyS0', 115200)
ser.timeout = 2.5
if not ser.is_open:
  ser.open()

ser.write(b'ate0\r')
ser.readline()
ser.write(b'at+cgpsinfo\r')
ser.readline()
ser.readline()
output = ser.readline()
if not output:
  output = "Got Nothing :("
  print(output)
  sys.exit()

output = output.decode(encoding='UTF-8')

if not output[0:11] == '+CGPSINFO: ':
  print ("Invalid response received from GPS Module")
  print(output)
  sys.exit()

output_redacted = output[11:]
output_l = output_redacted.split(',')
#print(output_l)

if len(output_l) < 4:
  print("Invalid response from GPS Module: {}".format(output_l))
  sys.exit()

lat = output_l[0]
lat_direction = output_l[1]
lon = output_l[2]
lon_direction = output_l[3]

#print("Latitude: {}{}, Longitude: {}{}".format(lat, lat_direction, lon, lon_direction))

#Split so I can extract las 2 digits before the .
lat_l = lat.split('.')
lon_l = lon.split('.')
lat_degrees = lat_l[0][:-2]
lon_degrees = lon_l[0][:-2]
#print("{}, {}".format(lat_degrees, lon_degrees))

#Convert the minutes part into float
lat_minutes = float(lat[len(lat_degrees):])
lon_minutes = float(lon[len(lon_degrees):])
#print("{}, {}".format(lat_minutes, lon_minutes))

#Convert the degrees to int
lat_degrees = int(lat_degrees)
lon_degrees = int(lon_degrees)

#Divide the minutes by 60
lon_minutes = lon_minutes/60
lat_minutes = lat_minutes/60

lon_out = lon_degrees + lon_minutes
lat_out = lat_degrees + lat_minutes

if lat_direction == 'S':
  lat_out = -lat_out
if lon_direction == 'W':
  lon_out = -lon_out

print("{}, {}".format(lat_out, lon_out))
