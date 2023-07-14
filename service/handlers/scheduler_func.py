from typing import Any, Dict

from aws_lambda_powertools.utilities.typing import LambdaContext

from service.handlers.schemas.env_vars import SchedulerEnvVars
from service.handlers.utils.env_vars_parser import get_environment_variables, init_environment_variables
from service.handlers.utils.observability import logger, tracer


@init_environment_variables(model=SchedulerEnvVars)
@tracer.capture_lambda_handler(capture_response=False)
def start_cron_job(event: Dict[str, Any], context: LambdaContext) -> None:
    logger.set_correlation_id(context.aws_request_id)

    env_vars: SchedulerEnvVars = get_environment_variables(model=SchedulerEnvVars)
    logger.debug('environment variables', extra=env_vars.model_dump())

    logger.info('finished handling cron event')
