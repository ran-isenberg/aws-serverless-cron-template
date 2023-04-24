from typing import Any, Dict

from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.parser import ValidationError, parse
from aws_lambda_powertools.utilities.parser.models import EventBridgeModel
from aws_lambda_powertools.utilities.typing import LambdaContext

from service.handlers.schemas.env_vars import RuleEnvVars
from service.handlers.utils.env_vars_parser import get_environment_variables, init_environment_variables
from service.handlers.utils.observability import logger, metrics, tracer


@init_environment_variables(model=RuleEnvVars)
@metrics.log_metrics
@tracer.capture_lambda_handler(capture_response=False)
def start_cron_job(event: Dict[str, Any], context: LambdaContext) -> None:
    logger.set_correlation_id(context.aws_request_id)

    env_vars: RuleEnvVars = get_environment_variables(model=RuleEnvVars)
    logger.debug('environment variables', extra=env_vars.dict())
    metrics.add_metric(name='CronTrigger', unit=MetricUnit.Count, value=1)

    try:
        # we want to extract and parse EventBridge event
        event_input: EventBridgeModel = parse(event=event, model=EventBridgeModel)
        logger.info('got input', extra=event_input.dict())
    except (ValidationError, TypeError) as exc:
        logger.error('event failed input validation', extra={'error': str(exc)})
        return

    metrics.add_metric(name='CronSuccessTrigger', unit=MetricUnit.Count, value=1)
    logger.info('finished handling cron event')
