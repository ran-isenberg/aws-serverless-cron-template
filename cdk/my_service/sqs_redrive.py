from aws_cdk import CfnResource, Duration
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_event_sources, aws_sqs
from constructs import Construct


class SqsRedrive(Construct):

    def __init__(self, scope: Construct, id_: str, sqs_lambda: _lambda.Function, dlq_lambda: _lambda.Function) -> None:
        super().__init__(scope, id_)
        dead_letter_queue = aws_sqs.Queue(
            self,
            f'{id_}dlq',
            queue_name=f'{id_}dlq',
            encryption=aws_sqs.QueueEncryption.SQS_MANAGED,
            retention_period=Duration.days(14),
        )
        main_queue: aws_sqs.Queue = aws_sqs.Queue(
            self,
            f'{id_}main',
            queue_name=f'{id_}main',
            encryption=aws_sqs.QueueEncryption.SQS_MANAGED,
            dead_letter_queue=aws_sqs.DeadLetterQueue(
                max_receive_count=3,  # max. number of times to retry processing a message before sending to the DLQ
                queue=dead_letter_queue,
            ),
            visibility_timeout=sqs_lambda.timeout,
        )

        self._create_scheduler_cron(id_, dlq_lambda)
        dlq_lambda.add_environment(key='SQS_ARN', value=main_queue.queue_arn)
        dlq_lambda.add_environment(key='DLQ_ARN', value=dead_letter_queue.queue_arn)

        # Add the SQS as an event source for the Lambda function
        sqs_lambda.add_event_source(aws_lambda_event_sources.SqsEventSource(main_queue))

    def _create_scheduler_cron(self, id_: str, dlq_lambda: _lambda.Function) -> CfnResource:
        scheduler_role = iam.Role(
            self,
            f'{id_}CronSchedulerRole',
            assumed_by=iam.ServicePrincipal('scheduler.amazonaws.com'),
            inline_policies={
                'invoke_target':
                    iam.PolicyDocument(statements=[
                        iam.PolicyStatement(
                            actions=['lambda:InvokeFunction'],
                            resources=[dlq_lambda.function_arn],
                            effect=iam.Effect.ALLOW,
                        )
                    ]),
            },
        )
        return CfnResource(
            self,
            f'{id_}MyScheduler',
            type='AWS::Scheduler::Schedule',
            properties={
                'Name': f'{id_}MyScheduler',
                'Description': 'Invoke the DLQ lambda between Sunday to Thursday at 23:00 Jerusalem (Israel) time',
                'FlexibleTimeWindow': {
                    'Mode': 'OFF'
                },
                'ScheduleExpression': 'cron(0 23 ? * SUN-THU *)',
                'ScheduleExpressionTimezone': 'Asia/Jerusalem',
                'Target': {
                    'Arn': dlq_lambda.function_arn,
                    'RoleArn': scheduler_role.role_arn,
                },
            },
        )
