from aws_cdk import RemovalPolicy
from constructs import Construct
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deploy
from pathlib import Path


class InputProducer(Construct):

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.bucket = self._create_bucket()
        self._upload_s3_objects(self.bucket)

    def _create_bucket(self) -> s3.Bucket:
        return s3.Bucket(
            self,
            f'{self.id_}PollyBucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

    def _upload_s3_objects(self, destination_bucket: s3.Bucket) -> None:
        current_path = Path(__file__).parent
        text_folder = current_path / ('text/')
        s3_deploy.BucketDeployment(
            self,
            f'{self.id_}PostDeployment',
            sources=[s3_deploy.Source.asset(str(text_folder))],
            destination_bucket=destination_bucket,
            prune=True,
        )
