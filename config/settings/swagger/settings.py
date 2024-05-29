SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "persistAuthorization": True,
    "PERSIST_AUTH": True,
    "VALIDATOR_URL": None,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}
