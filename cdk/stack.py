import os
from aws_cdk import Stack
from constructs import Construct
from secretsmanager.certificates import Secrets

from cdk.lambda_function.rossum_lambda import RossumLambda


class RossumStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        certificate = Secrets(self, 'Secrets')

        RossumLambda(self, 'Rossum Lambda', {"credentials": certificate.secret})

        self.add_tags()

    def add_tags(self):
        self.tags.set_tag('SERVICE', 'rossum-uko;')
        self.tags.set_tag('GIT_COMMIT', os.environ.get('GIT_COMMIT') or 'missing')
        self.tags.set_tag('GIT_REPOSITORY', '...')
        self.tags.set_tag('TEAM', '...')
        self.tags.set_tag('SBOM', 'yes')
        self.tags.set_tag('VERSION', os.environ.get('VERSION') | os.environ.get('GIT_COMMIT'))
