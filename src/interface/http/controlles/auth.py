from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import post, Request, Response, status_codes
from litestar.controller import Controller

from application.use_cases.login_user import LoginUserCommand, LoginUserUseCase
from application.use_cases.logout_user import LogoutUserCommand, LogoutUserUseCase
from application.use_cases.register_user import RegisterUserUseCase, RegisterUserCommand
from domain.value_objects.token_key import TokenKey
from domain.value_objects.username import Username
from interface.http.utils.response import make_error_response, make_data_response
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

        user = await register_user_use_case.execute(command=command)

        return UserSchema(username=user.username.as_generic_type(), id=user.id)

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
            user=UserSchema(username=user.username.as_generic_type(), id=user.id),
            token_key=TokenSchema(key=token_key.as_generic_type())
        )
        return response

    @post("/logout")
    @inject
    async def logout(
            self,
            request: Request,
            logout_user_use_case: FromDishka[LogoutUserUseCase],
    ) -> Response:
        raw_token_key = request.headers.get("authorization", None)

        if not raw_token_key:
            return make_error_response(status_code=status_codes.HTTP_401_UNAUTHORIZED, details="Missing Authorization header")

        token_key = TokenKey(value=raw_token_key)
        logout_command = LogoutUserCommand(token_key=token_key)

        await logout_user_use_case.execute(command=logout_command)

        return make_data_response(status_code=status_codes.HTTP_200_OK, message="Logged out successfully")
