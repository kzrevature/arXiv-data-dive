"""
Handler file for database management tasks.
Serves as an entry point for AWS Lambda.
"""

import json

from services.reset_db import reset_db


def handler(event, context):

    match (event["method"]):
        case "reset":
            res = reset_db_handler()
        case _:
            res = {
                "statusCode": 400,
                "body": json.dumps("Invalid method."),
            }

    return res


def reset_db_handler():
    reset_db()
    return {
        "statusCode": 200,
        "body": json.dumps("Article table dropped and recreated!"),
    }
