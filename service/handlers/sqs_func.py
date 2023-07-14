from typing import Any, Dict

from aws_lambda_powertools.utilities.batch import BatchProcessor, EventType, process_partial_response
from aws_lambda_powertools.utilities.batch.types import PartialItemFailureResponse
from aws_lambda_powertools.utilities.typing import LambdaContext

from service.handlers.schemas.sqs_input import OrderSqsRecord
from service.logic.handle_order import record_handler

processor = BatchProcessor(event_type=EventType.SQS, model=OrderSqsRecord)


def handle_sqs_batch(event: Dict[str, Any], context: LambdaContext) -> PartialItemFailureResponse:
    return process_partial_response(event=event, record_handler=record_handler, processor=processor, context=context)
