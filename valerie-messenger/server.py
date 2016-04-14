from flask import Flask, request
from flask import render_template
from flask_restful import Resource, Api
import json
import requests
from OpenSSL import SSL

context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')

app = Flask(__name__)
api = Api(app)

token = "CAACygOjEnAgBALPUwZCvbZClUW6sfQzhQgbr5hROUYMqGYF2dPCbuST6zCzyDIRjZB7egcJBBVj07z8RkLfP62ZBBOhcSZCIm954cky1KniIZAOMAw0CZAGbX2IZADIqZA6mgXm8H8FVven6TJSH2ZA9uGMz28DBgaTzmKcvWH5vCq7101Jiu6Ci4ZCgv98nQ2zbJ2jZAyGEOj89JAZDZD"

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Webhook(Resource):
    def get(self):
        token = request.args.get('hub.verify_token')
        if token == "TESTINGTOKEN":
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

api.add_resource(HelloWorld, '/')
api.add_resource(Webhook, '/webhook')



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=9999)