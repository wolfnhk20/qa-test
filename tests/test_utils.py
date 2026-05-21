import re

from utils import generate_request_id


def test_generate_request_id_returns_uuid4_string():
    request_id = generate_request_id()

    assert isinstance(request_id, str)
    assert re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", request_id)
