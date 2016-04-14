from flask import Flask, request
from flask import render_template
from flask_restful import Resource, Api
import json
import requests
import os

app = Flask(__name__)
api = Api(app)

token = os.environ.get('MESSENGER_TOKEN')
verify_token = os.environ.get('MESSENGER_VERIFY_TOKEN')


class Webhook(Resource):
    def get(self):
        token = request.args.get('hub.verify_token')
        if token == verify_token:
            return int(request.args.get('hub.challenge'))

    def post(self):
        # receives data from chat
        response = json.loads(request.data)
        print response
        user_id = response["entry"][0]['messaging'][0]['sender']['id']
        #recipient = response["entry"][0]['messaging'][0]['recipient']['id']
        #sender = json.loads(request.data)["entry"][0]['messaging'][0]['sender']['id']
        #message = json.loads(request.data)['entry'][0]['messaging'][0]["message"]["text"]        
        
        # if there is a message to response
        if 'message' in response["entry"][0]['messaging'][0]:
            # send a message to the user
            response = {
                'recipient': {
                    'id': user_id
                },
                'message': {
                    "text": "What's up!"
                }
            }
            #print "Returning message " + json.dumps(response)
            # return message
            request_uri = "https://graph.facebook.com/v2.6/me/messages?access_token="
            req = requests.post(request_uri, 
                                params={"access_token": token}, 
                                json=response
                                )


api.add_resource(Webhook, '/webhook')


if __name__ == "__main__":
    app.run(debug=True)
