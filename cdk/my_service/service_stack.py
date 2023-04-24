import os
from pathlib import Path

from aws_cdk import RemovalPolicy, Stack, Tags
from aws_cdk import aws_lambda as _lambda
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
from constructs import Construct
from git import Repo
from my_service.lambda_cron_rules import LambdaCronRuleConstruct  # type: ignore
from my_service.scheduler_cron import SchedulerCronConstruct  # type: ignore
from my_service.stepfunc_cron_rules import StepFuncCronRuleConstruct  # type: ignore

import cdk.my_service.constants as constants


def get_username() -> str:
    try:
        return os.getlogin().replace('.', '-')
    except Exception:
        return 'github'


def get_stack_name() -> str:
    repo = Repo(Path.cwd())
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
        lambda_layer = self._build_common_layer()
        self.lambdas_rule = LambdaCronRuleConstruct(self, self.shorten_construct_id('lambda_rule'), lambda_layer)
        self.state_func_rule = StepFuncCronRuleConstruct(self, self.shorten_construct_id('step_func_rule'))
        self.scheduler = SchedulerCronConstruct(self, self.shorten_construct_id('scheduler_lambda'), lambda_layer)

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
