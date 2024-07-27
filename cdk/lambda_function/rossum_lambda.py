import os
from aws_cdk import Duration, Fn, CfnParameter
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_secretsmanager as _secrets
from constructs import Construct


class RossumLambda(Construct):
    def __init__(self, scope: Construct, construct_id: str, secrets: dict[_secrets.Secret]):
        super().__init__(scope, construct_id)

        default_environment_variables = {
            'STAGE': Fn.import_value('main-stack:stage'),
            # can be dependent on stage
            'LOGLEVEL': 'WARN',
            'USERNAME': "username",
            'PASSWORD': secrets.get("credentials").secret_value.get("password"),  # value could be object
            'APP_URL': 'https://roucho-beranci-sro2.rossum.app/api/v1/',
            # if you do not mind slower lambda read the value in the code and not from env. Requires caching.
            'ROSSUM_API_KEY': secrets.get("api_key").secret_value,
            'UPLOAD_URL': "https://...",
        }

        rossum_role = iam.Role(
            self,
            'rossumRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')],
        )

        for secret in secrets.values():
            secret.grant_read(rossum_role)

        return _lambda.Function(
            self,
            'rossum-ukol',
            role=rossum_role,
            runtime=_lambda.Runtime.PYTHON_3_12,
            architecture=_lambda.Architecture.ARM_64,
            # point to the distribution
            code=_lambda.Code.from_asset('rossum-ukol/', exclude=['build', 'test']),
            handler='src.api.main.handler',
            function_name='rossum-ukol',
            layers=[],
            memory_size=1024,
            timeout=Duration.seconds(29),
            environment=default_environment_variables,
        )
