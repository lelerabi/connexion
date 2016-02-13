from mock import MagicMock
from connexion.decorators.security import get_tokeninfo_url, verify_oauth
from connexion.problem import problem

def test_get_tokeninfo_url(monkeypatch):
    env = {}
    monkeypatch.setattr('os.environ', env)
    security_def = {}
    assert get_tokeninfo_url(security_def) is None
    env['TOKENINFO_URL'] = 'issue-146'
    assert get_tokeninfo_url(security_def) == 'issue-146'
    env['HTTP_TOKENINFO_URL'] = 'foo'
    assert get_tokeninfo_url(security_def) == 'foo'
    security_def = {'x-tokenInfoUrl': 'bar'}
    assert get_tokeninfo_url(security_def) == 'bar'


def test_verify_oauth_invalid_auth_header(monkeypatch):
    def func():
        pass

    wrapped_func = verify_oauth('https://example.org/tokeninfo', set(['admin']), func)

    request = MagicMock()
    app = MagicMock()
    monkeypatch.setattr('connexion.decorators.security.request', request)
    monkeypatch.setattr('flask.current_app', app)
    resp = wrapped_func()
    assert resp == problem(401, 'Unauthorized', 'Invalid authorization header')
