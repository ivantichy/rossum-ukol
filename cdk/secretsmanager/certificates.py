from aws_cdk import SecretValue
import aws_cdk.aws_secretsmanager as _secrets
from constructs import Construct


class Secrets(Construct):
    def __init__(self, scope: Construct, construct_id: str):
        super().__init__(scope, construct_id)

        self.secret = _secrets.Secret(
            self,
            'Secret',
            secret_name='rossum-ukol-secret',
            secret_object_value={  # could be object, could be one value per secret
                'username': SecretValue.unsafe_plain_text('dummy_value'),
                'password': SecretValue.unsafe_plain_text('dummy_value'),
            },
        )
