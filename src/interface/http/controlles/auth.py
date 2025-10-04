from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import post
from litestar.controller import Controller

from application.use_cases.login_user import LoginUserCommand, LoginUserUseCase
from application.use_cases.register_user import RegisterUserUseCase, RegisterUserCommand
from domain.value_objects.username import Username
from interface.http.schemas.auth import UserRegistrationSchema, UserSchema, UserLoginSchema, LoginResponseSchema, \
    TokenSchema


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

    @post("/login")
    @inject
    async def login(
        self,
            data: UserLoginSchema,
            login_user_use_case: FromDishka[LoginUserUseCase]

    ) -> LoginResponseSchema:
        """
        User login endpoint.
        :param data: Payload data.
        :type data: UserLoginSchema
        :return: Public user schema.
        """
        command = LoginUserCommand(login=Username(data.login), password=data.password)

        user, auth_token, token_key = await login_user_use_case.execute(command=command)

        response = LoginResponseSchema(
            user=UserSchema(username=user.username.as_generic_type()),
            token_key=TokenSchema(key=token_key.as_generic_type())
        )
        return response