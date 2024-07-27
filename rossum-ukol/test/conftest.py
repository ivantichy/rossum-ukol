import os
import site
import requests_mock
import pytest

# quite important:
# we set our site dir to src to have proper package names
MODULE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
site.addsitedir(os.path.join(MODULE_DIR_PATH, '..', 'src'))


os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_SECURITY_TOKEN'] = 'testing'
os.environ['AWS_SESSION_TOKEN'] = 'testing'
os.environ['STAGE'] = 'testing'
os.environ['REGION'] = 'eu-central-1'
os.environ['AWS_REGION'] = 'eu-central-1'

os.environ['USERNAME'] = "user"
os.environ['PASSWORD'] = "f1a2c2c22053d3ebe072df74fb345ca1b2fee1846ba5a86b34c2bc230a830c87"
os.environ['APP_URL'] = "https://testdown/"
os.environ['ROSSUM_API_KEY'] = "yyyyyyyyyyyyyyyyyyyy"
os.environ['UPLOAD_URL'] = "https://testup"

import lambda_function
import config


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker(case_sensitive=False) as m, open('rossum-ukol/test/res/input.xml') as input:
        m.get('https://testdown/queues/1234/export?format=xml&id=5678', text=input.read(), status_code=200)
        m.post('https://testup', status_code=200)
        yield m
