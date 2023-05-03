import os
from pathlib import Path

from aws_cdk import Stack, Tags
from constructs import Construct
from git import Repo

from my_service.consumer import TextConsumer  # type: ignore
from my_service.producer import InputProducer  # type: ignore
import cdk.my_service.constants as constants


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
        self.input_producer = InputProducer(self, self.shorten_construct_id('PollyInput'))
        self.text_consumer = TextConsumer(self, self.shorten_construct_id('AudioMaker'))

    def shorten_construct_id(self, construct_name: str) -> str:
        return f'{self.id_}_{construct_name}'[0:64]
