from aws_cdk import Duration, aws_events, aws_events_targets
from aws_cdk import aws_stepfunctions as sfn
from constructs import Construct


class StepFuncCronRuleConstruct(Construct):

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.state_machine: sfn.StateMachine = self._create_state_machine()
        self.cron_rule: aws_events.Rule = self._create_cron_with_rule(self.state_machine)

    def _create_state_machine(self) -> sfn.StateMachine:
        # Create a state machine with a state that waits for 10 seconds and succeeds
        return sfn.StateMachine(
            self,
            f'{self.id_}MyStateMachine',
            definition=sfn.Wait(
                self,
                'MyState',
                time=sfn.WaitTime.duration(Duration.seconds(10)),
            ).next(sfn.Succeed(self, 'Done')),
        )

    def _create_cron_with_rule(self, target_state_machine: sfn.StateMachine) -> aws_events.Rule:
        # Create an EventBridge scheduler rule - invoke step func
        # between Monday to Friday at 6 PM UTC time
        return aws_events.Rule(
            self,
            f'{self.id_}MyDailyCronRule',
            schedule=aws_events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='MON-FRI',
            ),
            rule_name=f'{self.id_}MyDailyCronRule',
            targets=[aws_events_targets.SfnStateMachine(machine=target_state_machine)],
        )
