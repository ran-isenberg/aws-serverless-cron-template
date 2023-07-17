from typing import Any, Dict

import boto3
from aws_lambda_env_modeler import get_environment_variables, init_environment_variables
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError

from service.handlers.schemas.env_vars import DlqEnvVars
from service.handlers.utils.observability import logger


@init_environment_variables(model=DlqEnvVars)
def dlq_handler(event: Dict[str, Any], context: LambdaContext) -> None:
    logger.set_correlation_id(context.aws_request_id)

    env_vars: DlqEnvVars = get_environment_variables(model=DlqEnvVars)
    logger.debug('environment variables', extra=env_vars.model_dump())

    client = boto3.client('sqs')
    try:
        client.start_message_move_task(SourceArn=env_vars.DLQ_ARN, DestinationArn=env_vars.SQS_ARN)
        logger.info('finished handling dlq batch event')
    except ClientError as exc:
        logger.exception('unable to redrive dlq batch to sqs', extra={'error': str(exc)})
