import os
from pathlib import Path

from aws_cdk import Duration, RemovalPolicy, Stack, Tags
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
from constructs import Construct
from git import Repo
# from my_service.lambda_cron_rules import LambdaCronRuleConstruct  # type: ignore
# from my_service.scheduler_cron import SchedulerCronConstruct  # type: ignore
from my_service.sqs_redrive import SqsRedrive  # type: ignore

import cdk.my_service.constants as constants

# from my_service.stepfunc_cron_rules import StepFuncCronRuleConstruct  # type: ignore


def get_username() -> str:
    try:
        return os.getlogin().replace('.', '-')
    except Exception:
        return 'github'


def get_stack_name() -> str:
    repo = Repo(Path.cwd())
    # deepcode ignore NoHardcodedCredentials
    username = get_username()
    try:
        return f'{username}-{repo.active_branch}-{constants.SERVICE_NAME}'
    except TypeError:
        return f'{username}-{constants.SERVICE_NAME}'


class ServiceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.id_ = id
        Tags.of(self).add('schedule', constants.SERVICE_NAME)
        Tags.of(self).add('owner', get_username())
        self.layer = self._build_common_layer()
        self.target_lambda = self._create_target_lambda(self.layer)
        self.sqs_lambda = self._create_sqs_lambda(self.layer)
        self.dlq_lambda = self._create_dlq_lambda(self.layer)
        # self.lambdas_rule = LambdaCronRuleConstruct(self, self.shorten_construct_id('lambda_rule'), self.target_lambda)
        # self.state_func_rule = StepFuncCronRuleConstruct(self, self.shorten_construct_id('step_func_rule'))
        # self.scheduler = SchedulerCronConstruct(self, self.shorten_construct_id('scheduler_lambda'), self.target_lambda)
        self.redrive = SqsRedrive(self, self.shorten_construct_id('redrive'), self.sqs_lambda, self.dlq_lambda)

    def shorten_construct_id(self, construct_name: str) -> str:
        return f'{self.id_}_{construct_name}'[0:64]

    def _build_common_layer(self) -> PythonLayerVersion:
        return PythonLayerVersion(
            self,
            constants.LAMBDA_LAYER_NAME,
            entry=constants.COMMON_LAYER_BUILD_FOLDER,
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_10],
            removal_policy=RemovalPolicy.DESTROY,
        )

    def _create_target_lambda(self, lambda_layer: PythonLayerVersion) -> _lambda.Function:
        role = iam.Role(
            self,
            f'{self.id_}my_role',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name=('service-role/AWSLambdaBasicExecutionRole'))],
        )
        return _lambda.Function(
            self,
            f'{self.id_}SchedulerJob',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('.build/lambdas/'),
            handler='service.handlers.scheduler_func.start_cron_job',
            environment={
                'POWERTOOLS_SERVICE_NAME': 'cron',  # for logger, tracer and metrics
                'LOG_LEVEL': 'DEBUG',  # for logger
            },
            tracing=_lambda.Tracing.ACTIVE,
            retry_attempts=0,
            timeout=Duration.minutes(10),
            memory_size=128,
            layers=[lambda_layer],
            role=role,
            log_retention=aws_logs.RetentionDays.ONE_DAY,
        )

    def _create_sqs_lambda(self, lambda_layer: PythonLayerVersion) -> _lambda.Function:
        role = iam.Role(
            self,
            f'{self.id_}sqs',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name=('service-role/AWSLambdaBasicExecutionRole'))],
        )
        return _lambda.Function(
            self,
            f'{self.id_}SQS',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('.build/lambdas/'),
            handler='service.handlers.sqs_func.handle_sqs_batch',
            environment={
                'POWERTOOLS_SERVICE_NAME': 'sqs',  # for logger, tracer and metrics
                'LOG_LEVEL': 'DEBUG',  # for logger
            },
            tracing=_lambda.Tracing.ACTIVE,
            retry_attempts=0,
            timeout=Duration.seconds(30),
            memory_size=128,
            layers=[lambda_layer],
            role=role,
            log_retention=aws_logs.RetentionDays.ONE_DAY,
        )

    def _create_dlq_lambda(self, lambda_layer: PythonLayerVersion) -> _lambda.Function:
        role = iam.Role(
            self,
            f'{self.id_}dlq',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name=('service-role/AWSLambdaBasicExecutionRole'))],
            inline_policies={
                'redrive_policy':
                    iam.PolicyDocument(statements=[
                        iam.PolicyStatement(
                            actions=[
                                'sqs:StartMessageMoveTask', 'sqs:deletemessage', 'sqs:receivemessage', 'sqs:getqueueattributes', 'sqs:sendmessage'
                            ],
                            resources=['*'],  # not ideal, should be move specific to the actual queues
                            effect=iam.Effect.ALLOW,
                        )
                    ]),
            },
        )
        return _lambda.Function(
            self,
            f'{self.id_}DLQ',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('.build/lambdas/'),
            handler='service.handlers.dlq_func.dlq_handler',
            environment={
                'POWERTOOLS_SERVICE_NAME': 'dlq',  # for logger, tracer and metrics
                'LOG_LEVEL': 'DEBUG',  # for logger
            },
            tracing=_lambda.Tracing.ACTIVE,
            retry_attempts=0,
            timeout=Duration.seconds(30),
            memory_size=128,
            layers=[lambda_layer],
            role=role,
            log_retention=aws_logs.RetentionDays.ONE_DAY,
        )
