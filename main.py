from flask import Flask, request, make_response, jsonify
import os
import pprint
import json
from loguru import logger

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.proc.interaction_handler import InteractionHandler

PP = pprint.PrettyPrinter(indent=4)
API_HANDLER = TacoTuesdayApiHandler()

# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
IH = InteractionHandler(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)

# Dictionary to store taco orders. In the real world, you'd want an actual key-value store
TACO_ORDERS = {}

def get_arg(request, key):
    arg = request.form.get(key)
    logger.debug(key,':',arg)

    return arg

@app.route("/slack/interact/testytest", methods=["POST"])
def order_slash_command():
    for arg in request.args.keys():
        PP.pprint(request.args.get(arg))

    user_id = get_arg(request, 'user_id')
    channel_id = get_arg(request, 'channel_id')
    trigger_id = get_arg(request, 'trigger_id')

    IH.send_taco_modal(trigger_id)

    return make_response("", 200)


@app.route("/slack/interact", methods=["POST"])
def message_actions():
    logger.debug('At endpoint!')

    # Parse the request payload
    payload = json.loads(request.form["payload"])

    PP.pprint(payload)

    response = IH.handle_interaction(payload)
    if response: response = jsonify(response)
    logger.debug("Response: ", response)

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
