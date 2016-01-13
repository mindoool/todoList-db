from . import api
from application.models.post import Post


@api.route("/")
def test():
    return "hello"
