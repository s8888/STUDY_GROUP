from flask_restplus import Api, Resource, fields
from api_framework import create_app, register_init
from api_framework.utils import AppError

app = create_app(__name__)

api = Api(
    app,
    title="{{cookiecutter.project_name}}",
    version="1.0",
    description="{{cookiecutter.application_description}}",
    default="{{cookiecutter.project_name}}",
    default_label="{{cookiecutter.application_description}}",
)

fields_info = {
    "name": {
        "type_func": fields.String,
        "required": True,
        "description": "use error for demo error handler",
        "default": "World",
    }
}

basic_model = api.model(
    "Basic_Model",
    {key: value["type_func"](**value) for key, value in fields_info.items()},
)

resp_fields = api.model(
    "Response_Fields",
    {
        "returnCode": fields.Integer(description="服務是否有正常執行，正常執行為 0"),
        "message": fields.String(description="回傳內容"),
    },
)


def hello(name):
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
