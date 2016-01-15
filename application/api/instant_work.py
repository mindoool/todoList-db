# -*- coding: utf-8 -*-
from flask import request, jsonify, abort
from . import api
from application import db
from application.models.instant_work import InstantWork
from application.models.mixin import SerializableModelMixin
from application.lib.rest.auth_helper import required_token
from application.lib.encript.encript_helper import password_encode


# create
@api.route('/instant-works', methods=['POST'])
def create_instant_works():
    request_params = request.get_json()
    description = request_params.get('description')

    # TODO  regex, password validation need
    if description is None:
        return jsonify(
            userMessage="업무내용 입력을 확인해주세요."
        ), 400

    q = db.session.query(InstantWork).filter(InstantWork.description == description)

    if q.count() > 0:
        return jsonify(
            userMeesage="이미 등록된 업무입니다."
        ), 409

    try:
        instant_work = InstantWork(**request_params)

        db.session.add(instant_work)
        db.session.commit()

        return jsonify(
            data=instant_work.serialize()
        ), 200
    except:
        return jsonify(
            userMessage="업무 등록에 실패하였습니다."
        ), 403