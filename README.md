# TLDR;

`make docker-build docker-test`

No make?

`docker build -t rossum-ukol .` \
`docker run -it rossum-ukol make test`

# How to

## Install
`make install`

## Lock dependency versions
`make lock`

## Run tests locally
`make test`

## Format code
`make format`

## Run service locally on port 8000
`make run-local`

## Build Docker image
`make docker-build`

## Run tests in Docker 
`make docker-test`

## Run service in docker on port 8000
`make docker-run`

## Other
There are other targets that are related to AWS deployment but those are not functional - no AWS account linked. 

E.g. for deploy one would (actually some build engine) run:
`make deploy`

# Comments, findings:
- Docker is not enough. As part of the repository/code, there should be IaS. I added an example (it is not functional) of how I usually do lambda deployment with secrets.
- I added more than one test. Anyway, target coverage shall be >90%.
- As part of the PR/build test, there should be lint, format check, tests, and run CDK synth.
- Password is hashed. Anyway, I would not use a username and password. What I expected is that in the Rossum app, one would create an API key. Then I would put this API key into a secret. Also, I would expect to be able to revoke the key.
- No 2FA in the Rossum app?
- I did not add a pipeline definition (like Jenkinsfile).
- Bad user experience: The Rossum app has the same favicon as the documentation page. That is evil.
- Bad user experience: Trailing slash in the API URL. That stole half an hour of my life. At least sync your API behavior and documentation (used from Chrome). Better to accept both with and without the trailing slash.
- Bad user experience: The documentation. I had to search for parameters in the text (e.g., login).
- Bad user experience in the context of homework: If you ask for the app domain because you do not know why it does not work (trailing slash), it will send it to a timeouted temporary email.
- The welcome email has a username in the URL.
- Filtering parameters in the URL.
- Exported objects are missing IDs.
- I would rather implement it based on events in some state engine (AWS Step Functions) and make it eventually consistent.
