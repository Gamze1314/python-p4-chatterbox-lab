from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# enabled to share cross-origin requests/responses between browser and server.
CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


# handles GET request, POST request.
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    # GET / messages: returns an array of all messages as JSON, ordered by created_at in ascending order
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        response_body = [msg.to_dict() for msg in messages]
        return make_response(response_body, 200)

    elif request.method == 'POST':
        new_message = Message(
            # use json if you are sending JSON data.
            body=request.json.get("body"),
            username=request.json.get("username"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.session.add(new_message)
        db.session.commit()
        response_body = new_message.to_dict()
        return make_response(response_body, 201)  # status code for created.
    else:
        # status code for method not allowed.
        return make_response({"error": "Invalid request method"}, 405)



@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    # handles  UPDATE, DELETE requests.

    if request.method == 'PATCH':  # it is not updating but returning 200 response.
        message = Message.query.filter(Message.id == id).first()
        if message:
            #update the message 
            body = request.json.get('body') # data type being sent from front end is JSON and only updating the body.
            message.body = body
            db.session.add(message)
            db.session.commit()

            response_body = message.to_dict()
            return make_response(response_body, 200)
        else:
            return make_response({"error": "Message not found"}, 404)
        
    elif request.method == 'DELETE': #works properly.
        message = Message.query.filter(Message.id == id).first()
        if message:
            db.session.delete(message)
            db.session.commit()
            return make_response({"message": "Message deleted successfully"}, 200)
        else:
            return make_response({"error": "Message not found"}, 404)


if __name__ == '__main__':
    app.run(port=5555)
