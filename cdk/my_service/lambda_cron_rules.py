from aws_cdk import aws_events, aws_events_targets
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class LambdaCronRuleConstruct(Construct):

    def __init__(self, scope: Construct, id_: str, target_lambda: _lambda.Function) -> None:
        super().__init__(scope, id_)

        self.cron_rule = self._create_scheduled_cron_with_rule(id_, target_lambda)

    def _create_scheduled_cron_with_rule(self, id_: str, target_lambda: _lambda.Function) -> aws_events.Rule:
        return aws_events.Rule(
            self,
            f'{id_}MyLambdaCron',
            schedule=aws_events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='MON-FRI',
            ),
            targets=[aws_events_targets.LambdaFunction(handler=target_lambda,)],
            rule_name=f'{id_}MyLambdaCron',
        )
