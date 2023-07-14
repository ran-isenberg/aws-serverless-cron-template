from typing import Annotated, Literal

from pydantic import BaseModel, Field


class Observability(BaseModel):
    POWERTOOLS_SERVICE_NAME: Annotated[str, Field(min_length=1)]
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'ERROR', 'CRITICAL', 'WARNING', 'EXCEPTION']


class SqsEnvVars(Observability):
    ...


class DlqEnvVars(Observability):
    SQS_ARN: Annotated[str, Field(min_length=1)]
    DLQ_ARN: Annotated[str, Field(min_length=1)]


class SchedulerEnvVars(Observability):
    ...
