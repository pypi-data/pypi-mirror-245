from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme

from .authentication import LearngualAuthentication


class JWTScheme(SimpleJWTScheme):
    target_class = LearngualAuthentication
    name = ["JWTToken", "AccountId", "AccountIdX"]

    def get_security_definition(self, auto_schema):
        return [
            {
                "type": "http",
                "scheme": "bearer",
            },
            {"type": "apiKey", "in": "header", "name": "ACCOUNT"},
            {"type": "apiKey", "in": "header", "name": "X-ACCOUNT"},
        ]
