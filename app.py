from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

app.secret_key = "SECRETKEY"

app.config["MONGO_URI"] = "https://cloud.mongodb.com/v2/6112bc0e0706fa5ff929f52a#metrics/replicaSet/6112bd2b5ec8202779839f7e/explorer/COVID19/BedInfo/find"

mongo = PyMongo(app)


@app.route('/CreateBooking', methods=['POST'])
def CreateBooking():
    _json = request.json
    _PatientCriticalLevel = _json["Patient Critical Level"]
    _pincode = _json["Pincode"]
    _Hospital = _json["Hospital Name"]
    _TimeSlot = _json["Time Slot"]

    if _PatientCriticalLevel and _pincode and _Hospital and _TimeSlot and methods == 'POST':
        id = mongo.db.BedInfo.insert({'Patient Critical Level':_PatientCriticalLevel, 'Pincode':_pincode, 'Hospital Name': _Hospital, 'Time Slot': _TimeSlot})

        resp = jsonify("Booking Successful")
        resp.status_code = 200

        return resp

    else:
        return error404(404)

@app.route('/BedList')
def BedList():
    bed_list = mongo.db.BedInfo.find()

    resp = dumps(bed_list)

    return resp

@app.route('/BedList/<id>')
def showInfo(id):
    info = mongo.db.BedInfo.find_one({'_id': ObjectId(id)})
    
    resp = dumps(info)

    return resp

@app.route('/CancelBooking/<id>', methods = ['DELETE'])
def cancelBooking(id):
    mongo.db.BedInfo.delete_one({'_id': ObjectId(id)})
    resp = jsonify("Booking has been cancelled")
    resp.status_code = 200
    return resp

@app.route('/EditBooking/<id>', methods=['GET'])
def editBooking(id):
    _id = id
    _json = request.json
    _PatientCriticalLevel = _json["Patient Critical Level"]
    _pincode = _json["Pincode"]
    _Hospital = _json["Hospital Name"]
    _TimeSlot = _json["Time Slot"]

    if _PatientCriticalLevel and _pincode and _Hospital and _TimeSlot and methods == 'GET':
        id = mongo.db.BedInfo.insert({'Patient Critical Level':_PatientCriticalLevel, 'Pincode':_pincode, 'Hospital Name': _Hospital, 'Time Slot': _TimeSlot})

        resp = jsonify("Booking Successfully Edited")
        resp.status_code = 200

        return resp

    else:
        return error404(404)


@app.errorhandler(404)
def error404(error=None):
    msg = {'Status':404, 'msg':"Request not found"}

    resp = jsonify(msg)
    resp.status_code = 404

    return resp




if __name__ == "__main__":
    app.run(debug=True)