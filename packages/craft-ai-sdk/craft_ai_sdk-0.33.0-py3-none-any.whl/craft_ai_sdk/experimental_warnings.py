from enum import Enum
import functools
import warnings


WARNING_PREFIX = "\n\n    Warning:\n            "

MULTIPLE_EXPERIMENTAL_WARNING_MESSAGE = (
    "Multiple features are experimental and may behave unexpectedly:\n\n            * "
)
MULTIPLE_EXPERIMENTAL_WARNING_JOINER = "\n            * "

DEFAULT_EXPERIMENTAL_WARNING_MESSAGE = (
    "This feature is experimental and may behave unexpectedly. "
    "It may also be removed or changed in the future."
)


UPDATE_STEP_WARNING_MESSAGE = (
    "This feature is experimental and may behave unexpectedly. It is your "
    "responsibility to check the state and behavior of the step after an update. "
    "If the creation of the new step configuration takes more than roughly a "
    "minute, this function will return (time out) before the update terminated "
    "and you will need to check the step status manually at regular intervals. "
    "If several step updates are applies at the same time, "
    "the behavior is undefined."
)

DYNAMIC_DATASTORE_WARNING_MESSAGE = (
    "The dynamic datastore mapping is experimental and may be unstable."
)


class EXPERIMENTAL_VALUES(Enum):
    """Enumeration for experimental_parameters special values."""

    ALL = "ALL"
    STRING_CONTAINING = "STRING_CONTAINING"


def experimental(func_or_message):
    """Decorator to mark a function as experimental.

    Args:
        func_or_message (:obj:`str` :obj:`Nothing`): If a string is given, it will be
            used as a warning message. Else if nothing is given to the decorator
            (i.e. `@experimental`), a default warning message will be used.

    """

    def _get_wrapper(func, warning_message):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(warning_message, FutureWarning)
            return func(*args, **kwargs)

        doc_start, doc_separator, doc_end = func.__doc__.partition("\n\n")
        wrapper.__doc__ = (
            doc_start + WARNING_PREFIX + warning_message + doc_separator + doc_end
        )
        return wrapper

    if callable(func_or_message):  # No parameter is given
        func = func_or_message
        return _get_wrapper(func, DEFAULT_EXPERIMENTAL_WARNING_MESSAGE)
    else:  # A message is given
        warning_message = func_or_message
        return lambda func: _get_wrapper(func, warning_message)


def experimental_parameters(parameters):
    """Decorator to mark only some parameters of a function as experimental.

    Args:
        parameters (dict): A dictionary of parameters to be marked as
            experimental. The keys are the names of the parameters and the
            values are dictionaries with the following structure:
            {
                "value1": {"message": "message1"},
                "value2": {"message": "message2"},
                EXPERIMENTAL_VALUES.ALL: {"message": "message3"},
                EXPERIMENTAL_VALUES.STRING_CONTAINING: {
                    message: "message4",
                    substring: ["substring1", "substring2"],
                }
            }
            where the keys are the values of the parameters and the values are
            the messages to be displayed when the parameter is used.
            You can also use the `EXPERIMENTAL_VALUES.ALL` key to mark all the
            values of a parameter as experimental or
            `EXPERIMENTAL_VALUES.STRING_CONTAINING` to mark all the values of a
            parameter containing a string as experimental. In the latter case,
            you need to provide a `message` and a `substring` key in the
            dictionary value. The `message` will be displayed when the
            parameter is used with a value containing one of the strings in the
            `substring` list.

    """

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key, value in kwargs.items():
                if key in parameters:
                    if value in parameters[key]:
                        warnings.warn(
                            parameters[key][value]["message"],
                            FutureWarning,
                        )
                    elif EXPERIMENTAL_VALUES.ALL in parameters[key]:
                        warnings.warn(
                            parameters[key][EXPERIMENTAL_VALUES.ALL]["message"],
                            FutureWarning,
                        )
                    elif EXPERIMENTAL_VALUES.STRING_CONTAINING in parameters[key]:
                        if any(
                            substring in value
                            for substring in parameters[key][
                                EXPERIMENTAL_VALUES.STRING_CONTAINING
                            ]["substring"]
                        ):
                            warnings.warn(
                                parameters[key][EXPERIMENTAL_VALUES.STRING_CONTAINING][
                                    "message"
                                ],
                                FutureWarning,
                            )
            return func(*args, **kwargs)

        message_list = [
            value["message"] for key in parameters for value in parameters[key].values()
        ]
        if len(message_list) > 1:
            warning_message = f"{MULTIPLE_EXPERIMENTAL_WARNING_MESSAGE}\
{MULTIPLE_EXPERIMENTAL_WARNING_JOINER.join(message_list)}"
        else:
            warning_message = message_list[0]
        doc_start, doc_separator, doc_end = func.__doc__.partition("\n\n")
        wrapper.__doc__ = (
            f"{doc_start}{WARNING_PREFIX}{warning_message}{doc_separator}{doc_end}"
        )
        return wrapper

    return actual_decorator
