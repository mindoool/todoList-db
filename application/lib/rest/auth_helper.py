# coding: utf8
from inspect import getargspec
from functools import wraps
from traceback import print_exc
from flask import jsonify
from flask import request
from app import db
from app.models.user import User
from app.models.team import Team
from app.models.member import Member
from app.lib.jwt.jwt_helper import jwt_decode


def _get_user_from_request():
    """

    :param request:
    :return: sqlalchemy user query reusult object
    """
    token_string = request.headers.get('Authorization')
    decoded_data = jwt_decode(token_string)
    user_id = decoded_data.get("user_id")
    return db.session.query(User).get(user_id)


def required_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token_string = request.headers.get('Authorization')
        except:
            print_exc()
            return jsonify(
                userMessage="Authorization required"
            ), 401

        try:
            decoded_data = jwt_decode(token_string)
        except:
            print_exc()
            return jsonify(
                userMessage="invalid token",
                errorCode="1"
            ), 401

        decoded_user_id = decoded_data.get("user_id")
        if 'request_user_id' in getargspec(f).args:
            kwargs['request_user_id'] = decoded_user_id

        return f(*args, **kwargs)

    return decorated_function


def required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = _get_user_from_request()
        if user is None or user.is_admin == 0:
            return jsonify(
                userMessage="this request, admin authorization need"
            ), 401

        return f(*args, **kwargs)

    return decorated_function


def required_chair(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'member_id' not in kwargs and 'team_id' not in kwargs:
            return jsonify(
                userMessage="체어는 team_id, member_id가있는 url만 관리한다"
            ), 401

        user = _get_user_from_request()
        request_user_id = user.id
        if user.is_admin:  # 어드민은 프리페스
            return f(*args, **kwargs)

        if 'member_id' in kwargs:
            try:
                member_id = kwargs.get('member_id', 0)
                (member, team) = db.session.query(Member, Team) \
                    .join(Team, Team.id == Member.team_id) \
                    .filter(Member.id == member_id).one()

                if team.chair_user_id != request_user_id:
                    return jsonify(
                        userMessage="required chair authorization1"
                    ), 401
            except:
                return jsonify(
                    userMessage="required chair authorization2"
                ), 401

        if 'team_id' in kwargs:
            try:
                team_id = kwargs.get('team_id', 0)
                team = db.session.query(Team).get(team_id)
                if team.chair_user_id != request_user_id:
                    return jsonify(
                        userMessage="required chair authorization1"
                    ), 401

            except:
                return jsonify(
                    userMessage="required chair authorization4"
                ), 401

        return f(*args, **kwargs)

    return decorated_function
