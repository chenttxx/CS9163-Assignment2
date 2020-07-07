import pytest
import app as flask_app
import requests
from bs4 import BeautifulSoup

SITE = "http://localhost:5000/"

@pytest.fixture
def app():
    app = flask_app.create_app()
    app.debug = True
    return app.test_client()

def test_home_page(app):
    response = app.get(SITE)
    assert response.status_code == 200

def test_register_login_spellcheck(app):
    response = app.get(SITE + "register")
    assert response.status_code == 200
    app.post(SITE + 'register', data = {'uname':'user1', 'pword': 'user1', '2fa': '1234567890'})
    response = app.get(SITE + "register")
    assert response.status_code == 200

    app.post(SITE + 'login', data = {'uname':'user1', 'pword': 'user1', '2fa': '1234567890'})
    response = app.get(SITE + "login")
    assert response.status_code == 200

    app.get(SITE + "spell_check", data = {'inputtext':'hello kwkwkw what iwdak'})
    response = app.get(SITE + "spell_check")
    assert response.status_code == 200

def test_logout(app):
    response = app.get(SITE + "logout")
    assert response.status_code == 200

if __name__=="__main__":
    unittest.main()
    
