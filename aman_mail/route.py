class RouteController:
    def __init__(self, routing: dict):
        """
        Initializes the RouteController with a routing dictionary.
        """
        if not isinstance(routing, dict):
            raise ValueError("Routing must be a dictionary")
        self.routing = routing

    @staticmethod
    def _get_domain(email: str) -> str:
        """
        Extracts the domain from an email address.
        """
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        email = email.strip()
        if not email:
            raise ValueError("Email cannot be empty")
        if "@" not in email:
            raise ValueError("Email must contain '@' character")
        if email.count("@") > 1:
            raise ValueError("Email must contain only one '@' character")
        if "." not in email.split("@")[-1]:
            raise ValueError("Email domain must contain at least one '.' character")
        if email.startswith("@") or email.endswith("@"):
            raise ValueError("Email cannot start or end with '@' character")
        return email.split("@")[-1]

    def _get_route(self, email: str) -> dict:
        """
        Retrieves the routing information for a given email address.
        """
        domain = RouteController._get_domain(email)
        route = self.routing.get(domain)
        if not route:
            raise ValueError(f"No routing information found for domain: {domain}")
        return route

    def get_route_endpoint(self, email: str) -> str:
        """
        Retrieves the SMTP endpoint for a given email address.
        """
        route = self._get_route(email)
        if not route or "host" not in route or "port" not in route:
            raise ValueError(f"No valid route found for email: {email}")
        return route["host"], route["port"]

    def get_route_inbound_auth(self, email: str) -> dict:
        """
        Retrieves the inbound authentication credentials for a given email address.
        """
        route = self._get_route(email)
        if not route:
            raise ValueError(f"No route found for email: {email}")
        if "inbound_auth" not in route:
            return None
        inbound_auth = route.get("inbound_auth")
        if not inbound_auth:
            raise ValueError(
                f"No inbound authentication found for domain: {RouteController._get_domain(email)}"
            )
        return inbound_auth

    def get_route_outbound_auth(self, email: str) -> dict:
        """Retrieves the outbound authentication credentials for a given email address."""
        route = self._get_route(email)
        if not route:
            raise ValueError(f"No route found for email: {email}")
        if "outbound_auth" not in route:
            return None
        outbound_auth = route.get("outbound_auth")
        if not outbound_auth:
            raise ValueError(
                f"No outbound authentication found for domain: {RouteController._get_domain(email)}"
            )
        return outbound_auth
