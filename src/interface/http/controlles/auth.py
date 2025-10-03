from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import post
from litestar.controller import Controller

from application.use_cases.register_user import RegisterUserUseCase, RegisterUserCommand
from domain.value_objects.username import Username
from src.interface.http.schemas.auth import UserRegistrationSchema, UserSchema, UserLoginSchema


class AuthController(Controller):
    tags = ["Auth"]
    path = "/auth"

    @post("/register")
    @inject
    async def register(self, data: UserRegistrationSchema, register_user_use_case: FromDishka[RegisterUserUseCase]) -> UserSchema:
        """
        User registration endpoint.
        :param data: Payload data.
        :type data: UserRegistrationSchema
        :return: Public user schema.
        """
        command = RegisterUserCommand(username=Username(data.username), password=data.password)

        await register_user_use_case.execute(command=command)

        return UserSchema(username=data.username)
