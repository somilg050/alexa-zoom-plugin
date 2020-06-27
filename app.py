from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from jwt_tools import generate_jwt
from list_meetings import list_meetings
from start_meetings import change_meeting_status
from create_meetings import create_meetings


app = Flask(__name__)
api = Api(app)

@app.route("/integritycheck")
def main():
    return "Flask has been succesfully deployed using nginx"


class CreateJWT(Resource):
    def get(self):
        return jsonify(generate_jwt())


class ListMeetings(Resource):
    def get(self):
        pageno = request.args["pageno"]
        userid = request.args["userid"]
        jwt = request.headers.get("Authorization")
        return jsonify(list_meetings(pageno, userid, jwt))


class StartMeetings(Resource):
    def put(self):
        action = request.args["action"]
        jwt = request.headers.get("Authorization")
        meetingObj = request.get_json()
        return jsonify(change_meeting_status(jwt, action, meetingObj))


class CreateMeetings(Resource):
    def post(self):
        uuid = request.args["userid"]
        jwt = request.headers.get("Authorization")
        data = request.get_json()
        return jsonify(create_meetings(uuid, jwt, data))


api.add_resource(CreateJWT, "/jwt/create")
api.add_resource(ListMeetings, "/meetings/list")
api.add_resource(StartMeetings, "/meetings/start")
api.add_resource(CreateMeetings, "/meetings/create")

if __name__ == "__main__":
    app.run(debug=True)