from __future__ import unicode_literals

import warnings
from datetime import date, datetime
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Tuple, Union
from urllib.parse import quote_plus, urlencode

from loguru import logger

from orkg.logging_messages import MessageBuilder
from orkg.out import OrkgResponse, OrkgUnpaginatedResponse

if TYPE_CHECKING:
    from orkg.client.backend import ORKG  # Forward declaration only for type checking

# parts of URL to be omitted
SKIP_IN_PATH = (None, "", b"", [], ())


def _escape(value: Any) -> Any:
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # dates and datetimes into isoformat
    if isinstance(value, (date, datetime)):
        value = value.isoformat()

    # make bools into true/false strings
    elif isinstance(value, bool):
        value = str(value).lower()

    # don't decode bytestrings
    elif isinstance(value, bytes):
        return value

    if isinstance(value, (list, tuple)):
        return value
    return str(value)


def _make_path(*parts: Union[List, Tuple]) -> str:
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists and tuples to comma separated values.
    """
    return "/" + "/".join(
        # preserve ',' and '*' in url for nicer URLs in logs
        quote_plus(_escape(p), b",*")
        for p in parts
        if p not in SKIP_IN_PATH
    )


# parameters that apply to all methods
GLOBAL_PARAMS = ("pretty", "human", "error_trace", "format", "filter_path")


def query_params(*query_params):
    """
    Decorator that pops all accepted parameters from method's kwargs and puts
    them in the params argument.
    """

    def _wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            params = {}
            if "params" in kwargs:
                params = kwargs.pop("params").copy()
            for p in query_params + GLOBAL_PARAMS:
                if p in kwargs:
                    v = kwargs.pop(p)
                    if v is not None:
                        params[p] = _escape(v)

            # don't treat ignore and request_timeout as other params to avoid escaping
            for p in ("ignore", "request_timeout"):
                if p in kwargs:
                    params[p] = kwargs.pop(p)
            return func(*args, params=params, **kwargs)

        return _wrapped

    return _wrapper


def dict_to_url_params(params) -> str:
    return "?%s" % urlencode(params)


def simcomp_available(func):
    def check_if_simcomp_available(self: NamespacedClient, *args, **kwargs):
        if not self.client.simcomp_available:
            raise ValueError("simcomp_host must be provided in the ORKG wrapper class!")
        return func(self, *args, **kwargs)

    return check_if_simcomp_available


def admin_functionality(func):
    def display_admin_warning(self: NamespacedClient, *args, **kwargs):
        # TODO: create some functionality in the backend to check for permissions
        warnings.warn("This call needs elevated role in the system!", RuntimeWarning)
        return func(self, *args, **kwargs)

    return display_admin_warning


def check_host(func):
    """
    a decorator to check whether the backend is live or not.
    """

    def ping_decorator(self, *args, **kwargs):
        if not self.client.ping():
            raise ValueError("The ORKG is down!")
        return func(self, *args, **kwargs)

    return ping_decorator


class NamespacedClient(object):
    client: "ORKG"
    auth: Optional[dict]

    def __init__(self, client: "ORKG"):
        self.client = client
        if self.client.token is not None:
            self.auth = {"Authorization": f"Bearer {self.client.token}"}
        else:
            self.auth = None

    def __getattribute__(self, name: str) -> Any:
        """
        Logs any method called in the class or its children and the arguments passed to it
        """
        attr = object.__getattribute__(self, name)
        if not name.startswith("__") and callable(attr):

            def log_method_calls(*args, **kwargs):
                error = False
                # log when method is first called
                logger.debug(MessageBuilder.method_call(attr, name, args, kwargs))
                try:
                    return attr(*args, **kwargs)
                except Exception as e:
                    error = True
                    raise e
                finally:
                    if not error:
                        # log when method execution is complete
                        logger.debug(MessageBuilder.execution_complete(attr, name))

            return log_method_calls
        else:
            # return the attribute normally
            return attr

    @staticmethod
    def handle_sort_params(params: dict) -> None:
        if "sort" in params:
            sort_direction = "asc"
            if "desc" in params:
                sort_direction = "desc" if params["desc"] else "asc"
                del params["desc"]
            params["sort"] = f"{params['sort']},{sort_direction}"

    @staticmethod
    def _call_pageable(
        func: Callable[..., OrkgResponse],
        args: dict,
        params: dict,
        start_page: int = 0,
        end_page: int = -1,
    ) -> OrkgUnpaginatedResponse:
        def _call_one_page(page_number: int) -> Tuple[int, OrkgResponse]:
            try:
                params["page"] = page_number
                response = func(**args, params=params)
            except TypeError:
                # FIXME: check whether "func" is pageable without calling it !?
                raise ValueError(
                    'Provided "func" is either not pageable or the passed arguments are wrong'
                )

            if not response.succeeded:
                return 0, response

            if not response.page_info or "totalPages" not in response.page_info:
                raise ValueError('Provided "func" is not pageable')

            return response.page_info["totalPages"], response

        pages = []
        n_pages, page = _call_one_page(page_number=start_page)
        pages.append(page)

        if -1 < end_page < n_pages:
            n_pages = end_page

        for i in range(start_page + 1, n_pages):
            _, page = _call_one_page(page_number=i)
            pages.append(page)

        return OrkgUnpaginatedResponse(responses=pages)


def verb_logger(verb: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            if kwargs:
                logger.debug(
                    MessageBuilder.api_call_with_request_body(verb, args, kwargs)
                )
            else:
                logger.debug(MessageBuilder.api_call_simple(verb, args))

            return func(*args, **kwargs)

        return wrapper

    return decorator
