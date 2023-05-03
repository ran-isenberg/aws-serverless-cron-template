from service.handlers.processor import start
from tests.utils import generate_context


def test_text_process() -> None:
    start({}, generate_context())
