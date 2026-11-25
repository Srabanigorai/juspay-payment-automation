import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import pytest

from config.settings import ROOT
from pages.checkout_page import CheckoutPage
from pages.otp_page import OtpPage
from utils.data import load_test_data


class _Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def mock_server():
    """Serves mock_app/ on a free local port for the whole run."""
    handler = functools.partial(_Quiet, directory=str(ROOT / "mock_app"))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()


@pytest.fixture(scope="session")
def base_url(mock_server):
    return mock_server


@pytest.fixture(scope="session")
def data():
    return load_test_data()


@pytest.fixture
def checkout(page, base_url):
    c = CheckoutPage(page)
    c.open(base_url)
    c.proceed_to_pay()
    return c


@pytest.fixture
def otp(page):
    return OtpPage(page)
