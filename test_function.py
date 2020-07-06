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

def test_register(app):
    result = app.post("/register", data = {'unam': "user1", 
                                           'pword': "user1",
                                           '2fa': "1234567890")
    assert result.status_code == 200
    assert b'<div>Registration success!</div>' in result.data
    
                                           
    app.post("/register", data = {'unam': "user1", 
                                  'pword': "password",
                                  '2fa': "0123456789")
    result = app.get("/register")
    assert result.status_code == 200
   

