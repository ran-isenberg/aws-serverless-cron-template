from typing import Any, Dict

from aws_lambda_powertools.utilities.parser import BaseModel
from aws_lambda_powertools.utilities.parser.models import SqsRecordModel
from aws_lambda_powertools.utilities.parser.types import Json


class Order(BaseModel):
    item: Dict[str, Any]


class OrderSqsRecord(SqsRecordModel):
    body: Json[Order]  # deserialize order data from JSON string
