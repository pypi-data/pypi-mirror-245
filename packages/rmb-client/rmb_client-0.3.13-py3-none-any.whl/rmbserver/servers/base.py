from flask import request
from flask_restx import Api, Resource
from flask_httpauth import HTTPTokenAuth
from flask import Flask
from rmbserver import config




# 初始化web应用
app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = config.DEBUG
app.config.from_object('rmbserver.config')


api = Api(app, version='1.0', title='Reliable Meta Brain API',
          description='A simple private data analysis API'
          )

auth = HTTPTokenAuth(scheme='Bearer')


# 假设的有效令牌字典
tokens = {
    "token1": "user1",
    "token2": "user2"
}


# 认证回调函数
@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

