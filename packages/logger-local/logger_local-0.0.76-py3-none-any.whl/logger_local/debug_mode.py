import json
import os

from dotenv import load_dotenv

from .LoggerOutputEnum import LoggerOutputEnum
from .MessageSeverity import MessageSeverity

load_dotenv()

# TODO If there is no .logger.json file, please write to the console in which directory we should create it.
# TODO If there is .logger.json file (we support only one right?) , please write to the console the configuration.
# TODO Can we use SeverityLevelName instead of SeverityLevelId in the .logger.json? - Please add .logger.json.examples
# TODO Can we add the component name in addition to the component id in the .logger.json? - Please add .logger.json.examples
# TODO Can we add comments to the .logger.json file?

DEFAULT_MIN_SEVERITY = 600
LOGGER_CONFIGURATION_JSON = '.logger.json'
LOGGER_MINIMUM_SEVERITY = os.getenv('LOGGER_MINIMUM_SEVERITY')
DEBUG_EVERYTHING = False
LOGGER_JSON = {}


class DebugMode:
    @staticmethod
    def init():
        global LOGGER_MINIMUM_SEVERITY
        global LOGGER_JSON
        global DEBUG_EVERYTHING

        if LOGGER_MINIMUM_SEVERITY is None:  # Minimal severity in case there is not LOGGER_MINIMUM_SEVERITY environment variable
            LOGGER_MINIMUM_SEVERITY = DEFAULT_MIN_SEVERITY
            print(f"Using LOGGER_MINIMUM_SEVERITY={LOGGER_MINIMUM_SEVERITY} from Logger default "
                  "(can be overridden by LOGGER_MINIMUM_SEVERITY environment variable or .logger.json file per component and logger output")
        else:
            LOGGER_MINIMUM_SEVERITY = str(LOGGER_MINIMUM_SEVERITY)
            if hasattr(MessageSeverity, LOGGER_MINIMUM_SEVERITY):
                LOGGER_MINIMUM_SEVERITY = MessageSeverity[LOGGER_MINIMUM_SEVERITY].value
            elif LOGGER_MINIMUM_SEVERITY.isdigit():
                LOGGER_MINIMUM_SEVERITY = int(LOGGER_MINIMUM_SEVERITY)
            else:
                raise Exception("LOGGER_MINIMUM_SEVERITY must be a valid LoggerOutputEnum or a number or None")
            print("Using LOGGER_MINIMUM_SEVERITY=" + str(
                LOGGER_MINIMUM_SEVERITY) + " from environment variable. Can be overridden by .logger.json file per component and logger output.")
        try:
            with open(LOGGER_CONFIGURATION_JSON, 'r') as file:
                LOGGER_JSON = json.load(file)
        except FileNotFoundError:
            DEBUG_EVERYTHING = True
        # TODO MiniLogger.exception() in all exceptions
        except Exception:
            raise

    @staticmethod
    def is_logger_output(component_id: str, logger_output: LoggerOutputEnum, severity_level: int) -> bool:
        global DEBUG_EVERYTHING
        global LOGGER_MINIMUM_SEVERITY
        global LOGGER_JSON

        # Debug everything that has a severity level higher than the minimum required
        if DEBUG_EVERYTHING:
            result = severity_level >= LOGGER_MINIMUM_SEVERITY
            return result

        severity_level = max(severity_level, LOGGER_MINIMUM_SEVERITY)
        if component_id in LOGGER_JSON:
            output_info = LOGGER_JSON[component_id]
            if logger_output in output_info:
                result = severity_level >= output_info[logger_output]
                return result

        # In case the component does not exist in the logger configuration file or the logger_output was not specified
        result = True
        return result


# Call init() to initialize global variables used in is_logger_output
DebugMode.init()
