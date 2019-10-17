from flask import current_app
from flask_restplus import Api, Resource, fields, reqparse
from api_framework import create_app, register_init
from api_framework.utils import AppError

app = create_app(__name__)

api = Api(
    app,
    title="sample",
    version="1.0",
    description="sample api",
    default="sample",
    default_label="sample api",
)

fields_info = {
    "name": {
        "type_func": fields.String,
        "required": True,
        "description": "use error for demo error handler",
    },
    "gender": {
        "type_func": fields.String,
        "enum": ["male", "female"],
        "required": True,
    },
    "msg": {"type_func": fields.String, "default": "some msg~"},
    "aeg": {"type_func": fields.Integer, "required": True},
}

basic_model = api.model(
    "Basic_Model",
    {
        "name": fields.String(
            required=True, description="use error for demo error handler"
        ),
        "gender": fields.String(enum=["male", "female"], required=True),
        "msg": fields.String(default="some msg~"),
        "aeg": fields.Integer(required=True),
    },
)

resp_fields = api.model(
    "Response_Fields",
    {
        "returnCode": fields.Integer(description="服務是否有正常執行，正常執行為 0"),
        "message": fields.String(description="回傳內容"),
    },
)


def hello(name, **kwargs):
    if name == "error":
        raise ValueError("got some app error")
    else:
        return "Hello {}!".format(name)


@register_init(api, app)
def init_api(api, app):
    # TODO: API init
    app.logger.info(app.config.get("APP_CONFIG", {}))
    app.logger.info(api)
    pass


# TODO: implement your api
@api.route("/hello")
class Hello(Resource):
    @api.expect(basic_model, validate=True)
    @api.marshal_with(resp_fields, code=200, skip_none=True)
    def post(self):
        data = api.payload
        current_app.logger.debug(data)
        try:
            result = {"returnCode": 0, "message": hello(**data)}
            return result
        except Exception as e:
            raise AppError(e)


# form argparser
parser = reqparse.RequestParser()
# parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    "name",
    type=str,
    help="use error for demo error handler",
    required=True,
    location="form",
)

parser.add_argument(
    "gender", type=str, choices=["male", "female"], required=True, location="form"
)

parser.add_argument("msg", type=str, default="some msg~", location="form")

parser.add_argument("age", type=int, required=True, location="form")


@api.route("/hello_form")
class HelloForm(Resource):
    @api.expect(parser)
    @api.marshal_with(resp_fields, code=200, skip_none=True)
    def post(self):
        data = parser.parse_args()
        current_app.logger.debug(data)
        try:
            result = {"returnCode": 0, "message": hello(**data)}
            return result
        except Exception as e:
            raise AppError(e)


@api.errorhandler(AppError)
def app_error_handler(error):
    return ({"returnCode": -1}, getattr(error, "code", 200))


if __name__ == "__main__":
    app.init()  # pylint: disable=no-member
    app.run(host=app.config.get("HOST", "127.0.0.1"), port=app.config.get("PORT", 6001))

if __name__ != "__main__":
    app.init()  # pylint: disable=no-member
