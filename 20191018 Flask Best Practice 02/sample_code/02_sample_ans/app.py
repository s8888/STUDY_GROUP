from flask import current_app
from flask_restplus import Api, Resource, fields, inputs, reqparse
from api_framework import create_app, register_init
from api_framework.utils import AppError

app = create_app(__name__)

api = Api(
    app,
    title="sample",
    version="1.0",
    description="application_description",
    default="sample",
    default_label="application_description",
)

fields_info = {
    "type": {
        "type_func": fields.String,
        "required": True,
        "enum": ["IDB", "IDR", "LF", "LR", "RF", "RR"],
    },
    "base64_img": {"type_func": fields.String, "required": True},
    "return_img": {"type_func": fields.Boolean, "default": False},
}

basic_model = api.model(
    "Basic_Model",
    {key: value["type_func"](**value) for key, value in fields_info.items()},
)

result_fields = {
    "type": {
        "type_func": fields.String,
        "enum": ["IDB", "IDR", "LF", "LR", "RF", "RR"],
    },
    "result": {"type_func": fields.Boolean},
    "probability": {"type_func": fields.Float},
}

result_model = api.model(
    "Result_Model",
    {key: value["type_func"](**value) for key, value in result_fields.items()},
)

resp_fields = api.model(
    "Response_Fields",
    {
        "returnCode": fields.Integer(description="服務是否有正常執行，正常執行為 0"),
        "result": fields.Nested(result_model),
    },
)


def do_something(data):
    current_app.logger.debug(data)
    return {
        "returnCode": 0,
        "result": {"type": "IDB", "result": True, "probability": 0.95},
    }


@register_init(api, app)
def init_api(api, app):
    app.logger.info(app.config.get("APP_CONFIG", {}))
    app.logger.info(api)
    pass


@api.route("/hello")
class Hello(Resource):
    @api.expect(basic_model, validate=True)
    @api.marshal_with(resp_fields, code=200, skip_none=True)
    def post(self):
        data = api.payload
        try:
            return do_something(data)
        except Exception as e:
            raise AppError(e)


binary_form_fields_info = {
    "type": {
        "type": str,
        "location": "form",
        "required": True,
        "help": "類別名稱",
        "choices": ["IDB", "IDR", "LF", "LR", "RF", "RR"],
    },
    "base64_img": {"type": str, "location": "form", "required": True},
    "return_img": {"type": inputs.boolean, "location": "form", "default": False},
}
parser = reqparse.RequestParser(bundle_errors=True)
for key, value in binary_form_fields_info.items():
    parser.add_argument(key, **value)


@api.route("/hello_form")
class HelloForm(Resource):
    @api.expect(parser)
    @api.marshal_with(resp_fields, code=200, skip_none=True)
    def post(self):
        data = parser.parse_args()
        try:
            return do_something(data)
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
