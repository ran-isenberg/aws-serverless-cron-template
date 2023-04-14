from service.handlers.cron_job import start_cron_job
from service.handlers.schemas.input import Input
from tests.utils import generate_api_gw_event, generate_context


def test_cron_handler_success_flow(mocker):
    customer_name = 'RanTheBuilder'
    order_item_count = 5
    body = Input(customer_name=customer_name, order_item_count=order_item_count)
    start_cron_job(generate_api_gw_event(body.dict()), generate_context())
