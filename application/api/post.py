from . import api
from application.model.post import Post


@api.route("/")
def test():
    return "hello"
