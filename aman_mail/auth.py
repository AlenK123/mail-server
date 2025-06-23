from aiosmtpd.smtp import AuthResult, LoginPassword

from .route import RouteController


class Authenticator:
    def __init__(self, route_controller: RouteController):
        """
        Initializes the Authenticator with a RouteController instance.
        :param route_controller: An instance of RouteController to manage routing.
        """
        self.route_controller = route_controller

    def __call__(
        self, server, session, envelope, mechanism, login_password: LoginPassword
    ) -> bool:
        assert isinstance(login_password, LoginPassword)

        username = login_password.login.decode("utf-8")
        password = login_password.password.decode("utf-8")

        inbound_auth = self.route_controller.get_route_inbound_auth(username)

        if not inbound_auth:
            return AuthResult(success=True)
        if (
            inbound_auth
            and inbound_auth.get("username") == username
            and inbound_auth.get("password") == password
        ):
            return AuthResult(success=True)
        else:
            return AuthResult(success=False, handled=False)
