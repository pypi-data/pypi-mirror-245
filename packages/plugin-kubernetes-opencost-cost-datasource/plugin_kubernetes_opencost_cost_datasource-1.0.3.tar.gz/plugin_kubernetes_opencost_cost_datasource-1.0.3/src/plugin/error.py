from spaceone.core.error import ERROR_UNKNOWN, ERROR_INVALID_ARGUMENT


class ERROR_CONNECTOR_CALL_API(ERROR_UNKNOWN):
    _message = "API Call Error: {reason}"


class ERROR_EMPTY_BILLED_DATE(ERROR_UNKNOWN):
    _message = "Must have billed_date field or year, month fields.: {result}"


class ERROR_INVALID_PARAMETER_TYPE(ERROR_INVALID_ARGUMENT):
    _message = "Parameter type is invalid. (key = {key}, type = {type})"
