import os, codecs, simplejson, math, time
from urllib.request import urlopen
from urllib.parse   import quote

#-------------------------
# user-defined parameters
#-------------------------

GEOCODE  = 'https://maps.google.com/maps/api/geocode/json?address='
GEOCODE2 = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
KEY = 'AIzaSyCf5T9qpELsOHqXir6VON1nOC_NZU9q38o'
R = 6373000

#input file
in_1 = "input2a.txt"

#output file
out_1 = "czech_universe_output.txt"

#get the current working directory
workdir = os.getcwd()

input_1 = '{dir}/{file}'.format(dir=workdir, file=in_1)
output_1 = '{dir}/{file}'.format(dir=workdir, file=out_1)

#-----------------------------------------------------
# to read in a utf-16 file and write its content out
#-----------------------------------------------------

#define input file path
infile = input_1

#define output file path
outfile = output_1

#get handler to the file
fRead = codecs.open(infile,'r','utf-16') 
fWrite = codecs.open(outfile,'w','utf-16')
##fRead = open(infile,'r') 
##fWrite = open(outfile,'w')
i = 0

#read in input
with fRead as f_in:
    for l in f_in:
        i = i + 1
        if (i % 20 == 0):
            print(i)
        if i == 200:
            break
        #print(l)
        #print(i)
        #split the line into columns
        ss = l.split('\t')
        print(ss)
        #create query address
##        QueryAddr = ss[0] + '; "' + ss[6] + ' ' + ss[5] + ', ' + \
##                   ss[4] + ', ' + ss[8] + ', ' + 'Czech"; ' + \
##                   ss[23][:-2]
#        url_address = '"' + ss[3] + ', ' + ss[2] + ' ' + ss[1] + ',' + \
        url_address = '"' + ss[3] + ' ' + ss[2] + ',' + \
                   ss[1] + ',' + 'Czech"'
        url = GEOCODE + quote(url_address)  + "&sensor=false" + "&key=" + KEY
        time.sleep(0.2)
        print(url)
        result = simplejson.load(urlopen(url))
        if result['status'] == "ZERO_RESULTS":
            derived_latitude = "ZERO_RESULTS"
            derived_longitude = "ZERO_RESULTS"
            one_address = "ZERO_RESULTS"
        else:
            derived_latitude = simplejson.dumps([s['geometry']['location']['lat'] for s in result['results']][0], indent=2)
            derived_longitude = simplejson.dumps([s['geometry']['location']['lng'] for s in result['results']][0], indent=2)
            #print(derived_latitude)
            #print(derived_longitude)
            one_address = simplejson.dumps([s['formatted_address']for s in result['results']][0], ensure_ascii=False, indent=2)

        
        #Extract the longitude and latitude from string number 23. This will
        #be broken into four variables, e.g. N49 04.166 E16 27.973
        latitude =""
        longitude=""
        coords = ss[6].rsplit(' ')
        if (len(ss[6]) > 2):
##            latitude = float(coords[0][1:]) + ((float(coords[1]))/60.)
##            longitude = float(coords[2][1:]) + ((float(coords[3]))/60.)
            latitude = float(coords[1])
            longitude = float(coords[3])
            url = GEOCODE2 + str(latitude) +","+ str(longitude)  + "&key=" + KEY
            time.sleep(0.2)
            #print(url)
            result = simplejson.load(urlopen(url))
            address = simplejson.dumps([s['formatted_address']for s in result['results']][0], ensure_ascii=False, indent=2)
            #print(address)
            
        #write the line back to show reading and writing do not change content
        #fWrite.write(l+'\n')
        if (len(ss[6]) <= 2):
            fWrite.write(url_address + '; ' + str(latitude) + '; ' + str(longitude) + '; '
                         + derived_latitude +'; ' + derived_longitude + '; ; \n')
        else:
            if derived_longitude != "ZERO_RESULTS":
                dlon = math.radians(float(derived_longitude) - longitude)
                dlat = math.radians(float(derived_latitude) - latitude)
                a = (math.sin(dlat/2))**2 + math.cos(latitude) * math.cos(float(derived_latitude)) * (math.sin(dlon/2))**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                d = R * c
                print(d)
                fWrite.write(url_address + '; ' + str(latitude) + '; ' + str(longitude) + '; '
                             + derived_latitude +'; ' + derived_longitude + '; ' + address + '; ' +
                             str(round(d,2)) + " ; " + one_address + '\n')
            else:
                fWrite.write(url_address + '; ' + str(latitude) + '; ' + str(longitude) + '; '
                             + derived_latitude +'; ' + derived_longitude + '; ; ' + one_address + '\n')               

#house-keeping
print("Closing shop now...")
fRead.close()
fWrite.close()
