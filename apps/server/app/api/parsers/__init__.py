from http import HTTPStatus
import flask
from flask_restx import reqparse
from werkzeug import exceptions


def abort(code=HTTPStatus.INTERNAL_SERVER_ERROR, message=None, **kwargs):
    """
    Properly abort the current request.

    Raise a `HTTPException` for the given status `code`.
    Attach any keyword arguments to the exception for later processing.

    :param int code: The associated HTTP status code
    :param str message: An optional details message
    :param kwargs: Any additional data to pass to the error payload
    :raise HTTPException:
    """
    try:
        flask.abort(code)
    except exceptions.HTTPException as e:
        if message:
            errors = kwargs.pop("errors", None)
            kwargs["code"] = code.value
            kwargs["description"] = code.phrase
            kwargs["message"] = str(message)
            kwargs["errors"] = errors
        if kwargs:
            e.data = kwargs
        raise


# still the same functionality but now using the above abort function


class Argument(reqparse.Argument):
    def handle_validation_error(self, error, bundle_errors):
        error_str = str(error)
        error_msg = " ".join([str(self.help), error_str]) if self.help else error_str
        errors = {self.name: error_msg}

        if bundle_errors:
            return ValueError(error), errors
        abort(
            HTTPStatus.BAD_REQUEST,
            "Input payload validation failed",
            errors=errors,
        )


class RequestParser(reqparse.RequestParser):
    def __init__(self, argument_class=Argument):
        super().__init__(argument_class)

    def parse_args(self, req=None, strict=False):
        if req is None:
            req = flask.request

        result = self.result_class()

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        req.unparsed_arguments = (
            dict(self.argument_class("").source(req)) if strict else {}
        )
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                result[arg.dest or arg.name] = value

        if errors:
            abort(
                HTTPStatus.BAD_REQUEST,
                "Input payload validation failed",
                errors=errors,
            )

        if strict and req.unparsed_arguments:
            arguments = ", ".join(req.unparsed_arguments.keys())
            msg = "Unknown arguments: {0}".format(arguments)
            raise exceptions.BadRequest(msg)

        return result
