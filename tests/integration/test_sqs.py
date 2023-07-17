from typing import Any, Dict

from aws_lambda_powertools.utilities.typing import LambdaContext

from service.handlers.sqs_func import handle_sqs_batch


def generate_context() -> LambdaContext:
    context = LambdaContext()
    context._aws_request_id = '888888'
    return context


def generate_event() -> Dict[str, Any]:
    return {
        'Records': [{
            'messageId': '059f36b4-87a3-44ab-83d2-661975830a7d',
            'receiptHandle': 'AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a',
            'body': "{\"item\": {\"laptop\": \"amd\"}}",
            'attributes': {
                'ApproximateReceiveCount': '1',
                'SentTimestamp': '1545082649183',
                'SenderId': 'AIDAIENQZJOLO23YVJ4VO',
                'ApproximateFirstReceiveTimestamp': '1545082649185'
            },
            'messageAttributes': {},
            'md5OfBody': 'e4e68fb7bd0e697a0ae8f1bb342846b3',
            'eventSource': 'aws:sqs',
            'eventSourceARN': 'arn:aws:sqs:us-east-2: 123456789012:my-queue',
            'awsRegion': 'us-east-1'
        }, {
            'messageId': '244fc6b4-87a3-44ab-83d2-361172410c3a',
            'receiptHandle': 'AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a',
            'body': "{\"item\": {\"keyboard\": \"classic\"}}",
            'attributes': {
                'ApproximateReceiveCount': '1',
                'SentTimestamp': '1545082649183',
                'SenderId': 'AIDAIENQZJOLO23YVJ4VO',
                'ApproximateFirstReceiveTimestamp': '1545082649185'
            },
            'messageAttributes': {},
            'md5OfBody': 'e4e68fb7bd0e697a0ae8f1bb342846b3',
            'eventSource': 'aws:sqs',
            'eventSourceARN': 'arn:aws:sqs:us-east-2: 123456789012:my-queue',
            'awsRegion': 'us-east-1'
        }]
    }


def test_valid_sqs_batch() -> None:
    ret = handle_sqs_batch(generate_event(), generate_context())
    assert ret['batchItemFailures'] == []


def test_invalid_sqs_batch() -> None:
    event = generate_event()
    event['Records'][1]['body'] = 'invalid'
    ret = handle_sqs_batch(event, generate_context())
    assert len(ret['batchItemFailures']) == 1
