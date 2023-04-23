from aws_cdk import Duration, aws_events, aws_events_targets
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
from constructs import Construct

import cdk.my_service.constants as constants


class LambdaCronRuleConstruct(Construct):

    def __init__(self, scope: Construct, id_: str, lambda_layer: PythonLayerVersion) -> None:
        super().__init__(scope, id_)

        self.cron_lambda = self._create_rule_target_lambda(lambda_layer)
        self.cron_rule = self._create_scheduled_cron_with_rule(self.cron_lambda)

    def _create_scheduled_cron_with_rule(self, target_lambda: _lambda.Function) -> aws_events.Rule:
        return aws_events.Rule(
            self,
            'MyLambdaCron',
            schedule=aws_events.Schedule.rate(Duration.minutes(60)),
            targets=[aws_events_targets.LambdaFunction(handler=target_lambda,)],
            rule_name='MyLambdaCron',
        )

    def _build_cron_lambda_role(self) -> iam.Role:
        return iam.Role(
            self,
            constants.CRON_LAMBDA_ROLE_NAME,
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name=(f'service-role/{constants.LAMBDA_BASIC_EXECUTION_ROLE}'))
            ],
        )

    def _create_rule_target_lambda(self, lambda_layer: PythonLayerVersion) -> _lambda.Function:
        role = self._build_cron_lambda_role()
        return _lambda.Function(
            self,
            'CronJob',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset(constants.BUILD_FOLDER),
            handler='service.handlers.cron_job.start_cron_job',
            environment={
                constants.POWERTOOLS_SERVICE_NAME: constants.SERVICE_NAME,  # for logger, tracer and metrics
                constants.POWER_TOOLS_LOG_LEVEL: 'DEBUG',  # for logger
            },
            tracing=_lambda.Tracing.ACTIVE,
            retry_attempts=0,
            timeout=Duration.minutes(constants.API_HANDLER_LAMBDA_TIMEOUT),
            memory_size=constants.API_HANDLER_LAMBDA_MEMORY_SIZE,
            layers=[lambda_layer],
            role=role,
            log_retention=aws_logs.RetentionDays.ONE_DAY,
        )
