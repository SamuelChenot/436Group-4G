

def capture_id(uid, id):
    #send the id that was captured to the database
    print(uid)
    print(id)
    pass

def capture_zip(lat,lng):
    print(lat)
    print(lng)
    pass

def get_uid():
    f = open("uid.txt", "r")
    uid = f.read()
    return int(uid)

