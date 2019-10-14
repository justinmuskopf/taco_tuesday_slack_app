from flask import Flask, request, make_response, jsonify
import os
from pprint import pprint, pformat
import json
from loguru import logger

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.order import Order
from lib.proc.interaction_handler import InteractionHandler

API_HANDLER = TacoTuesdayApiHandler()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
IH = InteractionHandler(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)


def get_arg(request, key):
    arg = request.form.get(key)
    logger.debug(key,':',arg)

    return arg


@app.route("/slack/interact/order", methods=["POST"])
def order_slash_command():
    for arg in request.args.keys():
        pprint(request.args.get(arg))

    user_id = get_arg(request, 'user_id')
    channel_id = get_arg(request, 'channel_id')
    trigger_id = get_arg(request, 'trigger_id')

    IH.order(channel_id, trigger_id)

    return make_response("", 200)


@app.route("/slack/interact", methods=["POST"])
def message_actions():
    logger.debug('At endpoint!')

    # Parse the request payload
    payload = json.loads(request.form["payload"])

    logger.debug(pformat(f'Payload: \n{payload}'))

    response = IH.handle_interaction(payload)
    if response: response = jsonify(response)
    logger.debug("Response: ", response)

    return response


if __name__ == "__main__":
    taco_prices = TacoTuesdayApiHandler.get_tacos_from_api()

    Order.set_taco_prices(taco_prices)
    app.run(host='0.0.0.0')
