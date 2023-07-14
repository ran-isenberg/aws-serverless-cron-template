from typing import Any, Dict

from tenacity import RetryError, retry, stop_after_attempt, wait_exponential

from service.handlers.schemas.sqs_input import OrderSqsRecord
from service.handlers.utils.observability import logger


@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=4, max=10))
def retryable_logic(order: Dict[str, Any]) -> None:
    logger.info('finished handling record')


def record_handler(record: OrderSqsRecord) -> None:
    logger.info(record.body.item)
    try:
        retryable_logic(record.body.item)
    except RetryError as exc:
        logger.exception('reached retry limit, processing the item has failed', extra={'error': str(exc)})
        raise
