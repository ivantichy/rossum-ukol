import os
from aws_cdk import App
from stack import RossumStack


app = App()

RossumStack(app, 'Stack', stack_name=os.environ.get('STACK_NAME', 'rossum-ukol'))

app.synth()
