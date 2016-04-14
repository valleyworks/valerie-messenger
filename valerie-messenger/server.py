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
        sender = json.loads(request.data)["entry"][0]['messaging'][0]['sender']['id']
        message = json.loads(request.data)['entry'][0]['messaging'][0]["message"]["text"]

        try:

            response = {
                'recipient': {
                    'id': sender
                },
                'message': {
                    "text": message
                }
            }

            print "Returning message " + json.dumps(response)

            # return message
            req = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token":token},json=response)

        except Exception as e:
            raise e

api.add_resource(Webhook, '/webhook')


if __name__ == "__main__":
    app.run(debug=True)
