from typing import Any, Dict

from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.parser import ValidationError, parse
from aws_lambda_powertools.utilities.parser.envelopes import ApiGatewayEnvelope
from aws_lambda_powertools.utilities.typing import LambdaContext

from service.handlers.schemas.env_vars import CronEnvVars
from service.handlers.schemas.input import Input
from service.handlers.utils.env_vars_parser import get_environment_variables, init_environment_variables
from service.handlers.utils.observability import logger, metrics, tracer


@init_environment_variables(model=CronEnvVars)
@metrics.log_metrics
@tracer.capture_lambda_handler(capture_response=False)
def start_cron_job(event: Dict[str, Any], context: LambdaContext) -> None:
    logger.set_correlation_id(context.aws_request_id)

    env_vars: CronEnvVars = get_environment_variables(model=CronEnvVars)
    logger.debug('environment variables', extra=env_vars.dict())

    try:
        # we want to extract and parse the HTTP body from the api gw envelope
        input: Input = parse(event=event, model=Input, envelope=ApiGatewayEnvelope)
        logger.info('got create order request', extra={'order_item_count': input.order_item_count})
    except (ValidationError, TypeError) as exc:
        logger.error('event failed input validation', extra={'error': str(exc)})
        return

    metrics.add_metric(name='CronTrigger', unit=MetricUnit.Count, value=1)
    logger.info('finished handling event')
