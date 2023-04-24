
# AWS Serverless Cron Job Template (Python)

[![license](https://img.shields.io/github/license/ran-isenberg/aws-serverless-cron-template)](https://github.com/ran-isenberg/aws-serverless-cron-template/blob/master/LICENSE)
![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.10&color=blue?style=flat-square&logo=python)
![version](https://img.shields.io/github/v/release/ran-isenberg/aws-serverless-cron-template)
![github-star-badge](https://img.shields.io/github/stars/ran-isenberg/aws-serverless-cron-template.svg?style=social)
![issues](https://img.shields.io/github/issues/ran-isenberg/aws-serverless-cron-template)

![alt text](https://github.com/ran-isenberg/aws-serverless-cron-template/blob/main//banner.png?raw=true)

This project provides a working, open source based, Serverless cron jobs Python code including DEPLOYMENT code with CDK and a pipeline.

The project provides the following cron jobs:

1. AWS EventBridge rule cron job that triggers a lambda every X minutes
2. AWS EventBridge rule cron job that triggers a step function once a day at a specific time
3. AWS EventBridge scheduler cron job that triggers a lambda once a day

The AWS Lambda function use a logger, metrics, tracing, environment variables parsing and input validation best practices.

This project can serve as a template for new Serverless cron jobs or a as a reference. - CDK deployment code, pipeline and handler are covered.

**[Blogs website](https://www.ranthebuilder.cloud)**
> **Contact details | ran.isenberg@ranthebuilder.cloud**



### **Features**

- Python Serverless service with a recommended file structure.
- CDK infrastructure with infrastructure tests and security tests.
- CI/CD pipelines based on Github actions that deploys to AWS with python linters, static code analysis, complexity checks and style formatters.
- 3 different Serverless cron jobs including the new AWS EventBridge scheduler
- Unit, integration and E2E test folders ready for implementation.


## Serverless Best Practices
The AWS Lambda handler will implement multiple best practice utilities.

Each utility is implemented when a new blog post is published about that utility.

The utilities cover multiple aspect of a production-ready service, including:

- [Logging](https://www.ranthebuilder.cloud/post/aws-lambda-cookbook-elevate-your-handler-s-code-part-1-logging)
- [Observability: Monitoring and Tracing](https://www.ranthebuilder.cloud/post/aws-lambda-cookbook-elevate-your-handler-s-code-part-2-observability)
- [Observability: Business KPIs Metrics](https://www.ranthebuilder.cloud/post/aws-lambda-cookbook-elevate-your-handler-s-code-part-3-business-domain-observability)
- [Environment Variables](https://www.ranthebuilder.cloud/post/aws-lambda-cookbook-environment-variables)
- [Input Validation](https://www.ranthebuilder.cloud/post/aws-lambda-cookbook-elevate-your-handler-s-code-part-5-input-validation)
- [Dynamic Configuration & feature flags](https://www.ranthebuilder.cloud/post/aws-lambda-cookbook-part-6-feature-flags-configuration-best-practices)
- [Start Your AWS Serverless Service With Two Clicks](https://www.ranthebuilder.cloud/post/aws-lambda-cookbook-part-7-how-to-use-the-aws-lambda-cookbook-github-template-project)
- [CDK Best practices](https://github.com/ran-isenberg/aws-lambda-handler-cookbook)

## Getting started
### **Prerequisites**

* **Docker** - install [Docker](https://www.docker.com/){target="_blank"}. Required for the Lambda layer packaging process.
* **[AWS CDK](cdk.md)** - Required for synth & deploying the AWS Cloudformation stack.
* Python 10
* [poetry](https://pypi.org/project/poetry/){target="_blank"} - Make sure to run ``poetry config --local virtualenvs.in-project true`` so all dependencies are installed in the project '.venv' folder.
* For Windows based machines, use the Makefile_windows version (rename to Makefile). Default Makefile is for Mac/Linux.

### **Creating a Developer Environment**

1. Run ``make dev``
2. Run ``poetry install``

#### **Deploy CDK**

Create a cloudformation stack by running ``make deploy``.

### **Deleting the stack**

CDK destroy can be run with ``make destroy``.

### **Preparing Code for PR**

Run ``make pr``. This command will run all the required checks, pre commit hooks, linters, code formats, flake8 and tests, so you can be sure GitHub's pipeline will pass.

The command auto fixes errors in the code for you.

If there's an error in the pre-commit stage, it gets auto fixed. However, are required to run ``make pr`` again so it continues to the next stages.

Be sure to commit all the changes that ``make pr`` does for you.

### **Building dev/lambda_requirements.txt**

#### lambda_requirements.txt

CDK requires a requirements.txt in order to create a zip file with the Lambda layer dependencies. It's based on the project's poetry.lock file.

``make deploy` command will generate it automatically for you.

#### dev_requirements.txt

This file is used during GitHub CI to install all the required Python libraries without using poetry.

File contents are created out of the Pipfile.lock.

``make deploy`` ``make deps`` commands generate it automatically.



## Code Contributions
Code contributions are welcomed. Read this [guide.](https://github.com/ran-isenberg/aws-lambda-handler-cookbook/blob/main/CONTRIBUTING.md)

## Code of Conduct
Read our code of conduct [here.](https://github.com/ran-isenberg/aws-lambda-handler-cookbook/blob/main/CODE_OF_CONDUCT.md)

## Connect
* Email: [ran.isenberg@ranthebuilder.cloud](mailto:ran.isenberg@ranthebuilder.cloud)
* Blog Website [RanTheBuilder](https://www.ranthebuilder.cloud)
* LinkedIn: [ranisenberg](https://www.linkedin.com/in/ranisenberg/)
* Twitter: [IsenbergRan](https://twitter.com/IsenbergRan)

## Credits
* [AWS Lambda Handler Cookbook (Python)](https://github.com/ran-isenberg/aws-lambda-handler-cookbook)

## License
This library is licensed under the MIT License. See the [LICENSE](https://github.com/ran-isenberg/aws-lambda-handler-cookbook/blob/main/LICENSE) file.
