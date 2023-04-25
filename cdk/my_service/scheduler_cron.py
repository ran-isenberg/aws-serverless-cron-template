from aws_cdk import CfnResource
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class SchedulerCronConstruct(Construct):

    def __init__(self, scope: Construct, id_: str, target_lambda: _lambda.Function) -> None:
        super().__init__(scope, id_)
        self.cron_scheduler: CfnResource = self._create_scheduler_cron(id_, target_lambda)

    def _create_scheduler_cron(self, id_: str, target_lambda: _lambda.Function) -> CfnResource:
        scheduler_role = iam.Role(
            self,
            f'{id_}CronSchedulerRole',
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
            f'{id_}MyScheduler',
            type='AWS::Scheduler::Schedule',
            properties={
                'Name': f'{id_}MyScheduler',
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
