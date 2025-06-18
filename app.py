from flask import Flask, request,jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()



app = Flask(__name__) 

#enable corss-site request form any origin
CORS(app)


client =  MongoClient(os.getenv('MONGO_URI'))
db = client['InesBot']
roomsCollection = db['rooms']


# get all messages inside room with id
@app.route('/api/rooms/<string:room_id>/messages', methods=['GET'])
def getRoomMessages(room_id):
    messages = roomsCollection.find({"room_id":room_id})
            
    return jsonify({
        "code": 200,
        "success": True,
        "messages": [{
            "room_id": str(message['room_id']),
            "sender": message['sender'],
            "text": message['text'],
            "created_at": message['created_at'].isoformat()
        }
        for message in messages]
    }), 200
    


# push new message in the room with id
@app.route('/api/rooms/<string:room_id>/messages', methods=['POST'])
def pushMessages(room_id):
    message = {
        "room_id": room_id,
        'sender': request.json.get("sender"),
        "text": request.json.get("text"),
        "created_at": datetime.now()
    }
    
    roomsCollection.insert_one(message)
    return jsonify({
        "code": 201,
        "success": True,
    }), 201
    





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)









