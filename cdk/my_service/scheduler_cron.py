from aws_cdk import CfnResource, Duration
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
from constructs import Construct

import cdk.my_service.constants as constants


class SchedulerCronConstruct(Construct):

    def __init__(self, scope: Construct, id_: str, lambda_layer: PythonLayerVersion) -> None:
        super().__init__(scope, id_)
        self.target_lambda = self._create_scheduler_target_lambda(lambda_layer)
        self.cron_scheduler: CfnResource = self._create_scheduler_cron(self.target_lambda)

    def _create_scheduler_cron(self, target_lambda: _lambda.Function) -> CfnResource:
        scheduler_role = iam.Role(
            self,
            'CronSchedulerRole',
            assumed_by=iam.ServicePrincipal('scheduler.amazonaws.com'),
            inline_policies={
                'invoke_target':
                    iam.PolicyDocument(statements=[
                        iam.PolicyStatement(
                            actions=['lambda:InvokeFunction'],
                            resources=[target_lambda.function_arn],
                            effect=iam.Effect.ALLOW,
                        )
                    ]),
            },
        )
        # creates with low level cloud formation resource until issue is merged https://github.com/aws/aws-cdk-rfcs/issues/474
        return CfnResource(
            self,
            'MyScheduler',
            type='AWS::Scheduler::Schedule',
            properties={
                'Name': 'MyScheduler',
                'Description': 'Invoke a lambda between Sunday to Thursday at 10 AM Jerusalem (Israel) time',
                'FlexibleTimeWindow': {
                    'Mode': 'OFF'
                },
                'ScheduleExpression': 'cron(0 10 ? * SUN-THU *)',
                'ScheduleExpressionTimezone': 'Asia/Jerusalem',
                'Target': {
                    'Arn': target_lambda.function_arn,
                    'RoleArn': scheduler_role.role_arn,
                },
            },
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

    def _create_scheduler_target_lambda(self, lambda_layer: PythonLayerVersion) -> _lambda.Function:
        role = self._build_cron_lambda_role()
        return _lambda.Function(
            self,
            'SchedulerJob',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset(constants.BUILD_FOLDER),
            handler='service.handlers.scheduler_func.start_cron_job',
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
