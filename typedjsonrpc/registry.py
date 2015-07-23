"""This module contains logic for storing and calling jsonrpc methods."""
import json


__all__ = ["Registry"]


class Registry(object):
    """The registry for storing and calling jsonrpc methods."""

    def __init__(self):
        self._name_to_method = {}

    def dispatch(self, request):
        """Takes a request and dispatches its data to a jsonrpc method.

        :param request: a werkzeug request with json data
        :type request: werkzeug.wrappers.Request

        :returns: json output of the corresponding function
        :rtype: str
        """
        msg = json.loads(request.get_data())
        func = self._name_to_method[msg["method"]]
        if isinstance(msg["params"], list):
            return json.dumps(func(*msg["params"]))
        elif isinstance(msg["params"], dict):
            return json.dumps(func(**msg["params"]))
        else:
            raise Exception("Invalid params type")

    def register(self, name, method):
        """Registers a method with a given name.

        :param name: The name to register
        :type name: str
        :param method: The function to call
        :type method: function
        """
        self._name_to_method[name] = method

    def method(self):
        """Syntactic sugar for registering a method"""
        def wrapper(func):
            """Registers a method with its fully qualified name.

            :param func: The function to register
            :type func: T
            :returns: The original function unmodified
            :rtype: T
            """
            fully_qualified_name = "{}.{}".format(func.__module__, func.__name__)
            self._name_to_method[fully_qualified_name] = func
            return func

        return wrapper