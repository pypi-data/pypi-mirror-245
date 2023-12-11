from wheke import Pod

from wheke_auth.cli import cli
from wheke_auth.routes import router
from wheke_auth.service import AuthService, auth_service_factory

auth_pod = Pod(
    "auth",
    router=router,
    services=[(AuthService, auth_service_factory)],
    cli=cli,
)
