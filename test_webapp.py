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
    res = app.get(SITE)
    assert res.status_code == 200

def test_register_page(app):
    res = app.get(SITE + "register")
    assert res.status_code == 200

def test_login_page(app):
    res = app.get(SITE + "login")
    assert res.status_code == 200

def test_spellcheck_page(app):
    res = app.get(SITE + "spellcheck")
    assert res.status_code == 200

if __name__=="__main__":
    
