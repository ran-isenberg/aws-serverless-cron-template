from aws_cdk import aws_lambda as _lambda
from constructs import Construct
from cdk.my_service import constants
from aws_cdk import Duration, RemovalPolicy
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion


class TextConsumer(Construct):

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)
        self.id_ = id_

    def _build_common_layer(self) -> PythonLayerVersion:
        return PythonLayerVersion(
            self,
            constants.LAMBDA_LAYER_NAME,
            entry=constants.COMMON_LAYER_BUILD_FOLDER,
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_10],
            removal_policy=RemovalPolicy.DESTROY,
        )

    def _create_target_lambda(self) -> _lambda.Function:
        lambda_layer = self._build_common_layer()
        role = iam.Role(
            self,
            f'{self.id_}my_role',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name=('service-role/AWSLambdaBasicExecutionRole'))],
        )
        return _lambda.Function(
            self,
            f'{self.id_}TextConsumer',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('.build/lambdas/'),
            handler='service.handlers.processor.start',
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
