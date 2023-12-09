import requests
from peucr_core.validator import TestValidator
from peucr_core.exceptions import InvalidDefinitionException

class DefaultValidator(TestValidator):

    def __init__(self):
        self.labels = ["DEFAULT"]


    def apply(self, expectation, response, suite):
        if "success" not in response:
            raise InvalidDefinitionException("No \"success\" field in response")

        msg = response["msg"] if response.get("msg") else ""

        return {"success": response["success"], "msg": msg}
