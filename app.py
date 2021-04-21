import random
from datetime import datetime

from flask import Flask, request, make_response, jsonify
from pprint import pprint, pformat
from loguru import logger
import json
import os

from config.config_parser import TacoTuesdayConfigParser
from config.system_config import TacoTuesdaySystemConfig
from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.proc.handler.employee import EmployeeHandler
from lib.proc.handler.error import ErrorHandler
from lib.proc.handler.interaction import InteractionHandler
from lib.proc.handler.running_order import RunningOrderHandler
from lib.proc.handler.view import ViewHandler

TacoTuesdayConfigParser.parse()
API_HANDLER = TacoTuesdayApiHandler()
IH = InteractionHandler()

# Flask web server for incoming traffic from Slack
app = Flask(__name__)


def get_arg(_request, key):
    arg = _request.form.get(key)
    logger.debug(key, ':', arg)

    return arg

@app.route("/slack/interact/admin", methods=["POST"])
def admin_slash_command():
    denials = [
        "Yeah. Like I'd ever let you do that.",
        "You do not have access to this command!",
        "Don't make me tell on you.",
        "You are not in the sudoers file. This incident will be reported."
    ]

    denial = random.choice(denials)

    slack_id = get_arg(request, 'user_id')
    channel_id = get_arg(request, 'channel_id')
    trigger_id = get_arg(request, 'trigger_id')
    text = get_arg(request, 'text').lower()

    try:
        employee = API_HANDLER.get_employee_by_slack_id(slack_id)

        if not employee.admin:
            return make_response(denial, 200)

        IH.admin(trigger_id)

        return make_response("", 200)
    except Exception as e:
        ErrorHandler.handle(e)


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

        return make_response("", 200)
    except Exception as e:
        return ErrorHandler.handle(e)

@app.route("/slack/interact", methods=["POST"])
def message_actions():
    try:
        # Parse the request payload
        payload = json.loads(request.form["payload"])

        logger.debug(pformat(f'Payload: \n{payload}'))

        response = IH.handle_interaction(payload)
        if response: response = jsonify(response)

        return response
    except Exception as e:
        return ErrorHandler.handle(e)


if __name__ == "__main__":
    from pathlib import Path

    logger.add(sink=Path(TacoTuesdaySystemConfig().get_log_dir(), '{time}.log'), rotation="00:00")

    app.run(host='0.0.0.0')
