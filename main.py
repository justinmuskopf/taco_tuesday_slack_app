from datetime import datetime

from flask import Flask, request, make_response, jsonify
from pprint import pprint, pformat
from loguru import logger
import json
import os

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.proc.handler.employee import EmployeeHandler
from lib.proc.handler.interaction import InteractionHandler
from lib.proc.handler.running_order import RunningOrderHandler
from lib.proc.handler.view import ViewHandler

API_HANDLER = TacoTuesdayApiHandler()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
LOG_DIR = os.environ['TT_SLACK_LOG_DIR']
IH = InteractionHandler(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)


def get_arg(_request, key):
    arg = _request.form.get(key)
    logger.debug(key, ':', arg)

    return arg


@app.route("/slack/interact/order", methods=["POST"])
def order_slash_command():
    for arg in request.args.keys():
        pprint(request.args.get(arg))

    slack_id = get_arg(request, 'user_id')
    channel_id = get_arg(request, 'channel_id')
    trigger_id = get_arg(request, 'trigger_id')
    text = get_arg(request, 'text').lower()

    try:
        if text == 'cancel':
            if not RunningOrderHandler.has_employee_order(slack_id):
                EmployeeHandler.discipline_employee(slack_id, channel_id, "You haven't placed an order yet you goober!")
            else:
                ViewHandler.send_order_cancel_modal(trigger_id)
        else:
            IH.order(channel_id, trigger_id)
    except Exception as e:
        logger.error(f'Caught bubbled up: {e}')
        return make_response(str(e), 200)

    return make_response("", 200)


@app.route("/slack/interact", methods=["POST"])
def message_actions():
    # Parse the request payload
    payload = json.loads(request.form["payload"])

    logger.debug(pformat(f'Payload: \n{payload}'))

    response = IH.handle_interaction(payload)
    if response: response = jsonify(response)

    return response


if __name__ == "__main__":
    from pathlib import Path

    logger.add(sink=Path(LOG_DIR, '{time}.log'), rotation="00:00")

    app.run(host='0.0.0.0')
