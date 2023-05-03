from typing import Any, Dict

from aws_lambda_powertools.utilities.typing import LambdaContext

from service.handlers.schemas.env_vars import SchedulerEnvVars
from service.handlers.utils.env_vars_parser import get_environment_variables, init_environment_variables
from service.handlers.utils.observability import logger, tracer
from service.logic.consume_text import consume_text, consume_text_async


@init_environment_variables(model=SchedulerEnvVars)
@tracer.capture_lambda_handler(capture_response=False)
def start(event: Dict[str, Any], context: LambdaContext) -> None:
    logger.set_correlation_id(context.aws_request_id)
    logger.info('starting to handle text processor event')

    env_vars: SchedulerEnvVars = get_environment_variables(model=SchedulerEnvVars)
    logger.debug('environment variables', extra=env_vars.dict())
    consume_text_async()
    logger.info('finished handling text processor event')
