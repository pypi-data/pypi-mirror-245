import time
import sys
from peucr_core.loaders import ConfigLoader, SpecLoader, PluginLoader, ValidatorLoader
from peucr_core.exceptions import InvalidDefinitionException


class TestFramework:
    def __init__(self, args):
        self.separator = "**************************************************"
        self.retryInterval = 0.2
        self.config = ConfigLoader(args).apply()
        self.specs = SpecLoader(self.config).apply()
        self.plugins = PluginLoader(self.config).apply()
        self.validators = ValidatorLoader(self.config).apply()



    def exec_actions(self, actions, data):
        if data["error"] or actions is None or len(actions) == 0:
            return data

        success = False

        for action in actions:
            success = False
            startTime = time.time()

            while not success and time.time() - startTime < 2:
                try:
                    success = self.plugins.apply(action)["success"]

                except Exception as e:
                    data["error"] = True
                    data["msg"] = "Action failed.", e

                if success or data["error"]:
                    break

                time.sleep(self.retryInterval)

        return data



    def exec_validation(self, validation, data):
        if data["error"]:
            return data

        time.sleep(validation.get("wait", 0))

        attempts = min(5, validation.get("duration", self.retryInterval)) / self.retryInterval
        counter = 0
        result = {"success": False}

        while not result["success"] and counter < attempts:
            try:
                response = self.plugins.apply(validation)
                result = self.validators.apply(validation.get("expectation"), response)

            except InvalidDefinitionException as e:
                data["msg"] = e
                break

            except Exception as e:
                data["msg"] = "Error:", e

            if result["success"]:
                break

            time.sleep(self.retryInterval)
            counter += 1

        if not result["success"]:
            data["msg"] = "Failure.", result.get("msg", "")
            data["error"] = True

        return data



    def exec_validations(self, validations):
        if data["error"]:
            return data

        if not validations or not isinstance(validations, list) or len(validations) == 0:
            data["error"] = True
            data["msg"] = "No validation specified in test. Aborting."
            return data

        for validation in validations:
            data = self.exec_validation(validation, data)

        return data



    def exec_test(self, spec):
        data = {"name": spec.get("name", "UNNAMED"), "start": time.time(), "error": False, "type": "test"}

        data = self.exec_actions(spec.get("context"), data)
        data = self.exec_actions(spec.get("actions"), data)
        data = self.exec_validations(spec.get("validation"), data)

        data["end"] = time.time()

        self.print_report(data)
        return data



    def exec_test_suite(self, specs):
        successes = 0

        results = [self.exec_test(spec) for spec in specs]

        for result in results:
            if not result["error"]:
                successes += 1

        print(self.separator)

        if successes != len(specs):
            print(len(specs), "tests run", len(specs) - successes, "failures")
            sys.exit(1)        

        print(len(specs), "tests run. No failures.")



    def exec_preconditions(self, validations):
        if validations is None or validations.get("validation") is None:
            return

        for validation in validations["validation"]:
            data = {"name": validation.get("name", "UNNAMED"), "type": "precondition", "start": time.time(), "error": False}

            data = self.exec_validation(validation, data)

            if data["error"]:
                data["msg"] = "Precondition validation failed. Test will be aborted"

            data["end"] = time.time()

            self.print_report(data)

            if data["error"]:
                sys.exit(1)

        print(self.separator)


    
    def print_report(self, data):
        if data["type"] == "precondition":
            print("Verifying {:s} - {:.3f}s".format(data["name"], data["end"]-data["start"]))
            if data["error"] and data["msg"]:
                print(data["msg"])

        if data["type"] == "test":
            print(data)



    def exec(self):
        self.exec_preconditions(self.specs.get("preconditions"))
        self.exec_test_suite(self.specs.get("execution"))
