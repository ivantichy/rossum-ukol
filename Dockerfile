# TODO homework for you - why the hell Node?
# TODO use common (Rossum) docker image
FROM node:20 

ENV USERNAME=myUser123 PASSWORD=d14f69b3218c54b0eb818c15e1fcc0b54e4cfa32599f6bbcb58380c99ed8b8b4 APP_URL=https://roucho-beranci-sro2.rossum.app/api/v1/ \
    ROSSUM_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx UPLOAD_URL=https://www.postb.in/1721988252220-3278229255229 LOGLEVEL=DEBUG

# TODO shall we run update/upgrade?
# What is wrong here ? Two things
RUN apt update -y && \ 
    apt install -y python3 pip zip && \
    curl https://pyenv.run | bash

# --break-system-packages allows to install packages globally (ignores externally-managed-environment switch)
# Is it correct to split RUN into multiple commands?
RUN pip install awscli pipenv --break-system-packages && \ 
    npm install -g aws-cdk

WORKDIR /app

COPY . .

RUN make install

ENTRYPOINT []


