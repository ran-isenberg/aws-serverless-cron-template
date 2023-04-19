
# AWS Serverless Cron Job Template (Python)

[![license](https://img.shields.io/github/license/ran-isenberg/aws-serverless-cron-template)](https://github.com/ran-isenberg/aws-serverless-cron-template/blob/master/LICENSE)
![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.10&color=blue?style=flat-square&logo=python)
[![codecov](https://codecov.io/gh/ran-isenberg/aws-serverless-cron-template/branch/main/graph/badge.svg?token=P2K7K4KICF)](https://codecov.io/gh/ran-isenberg/aws-serverless-cron-template)
![version](https://img.shields.io/github/v/release/ran-isenberg/aws-serverless-cron-template)
![github-star-badge](https://img.shields.io/github/stars/ran-isenberg/aws-serverless-cron-template.svg?style=social)
![issues](https://img.shields.io/github/issues/ran-isenberg/aws-serverless-cron-template)

![alt text](https://github.com/ran-isenberg/aws-serverless-cron-template/blob/main/docs/media/banner.png?raw=true)

This project provides a working, open source based, AWS Lambda handler skeleton Python code including DEPLOYMENT code with CDK and a pipeline.

This project can serve as a template for new Serverless services - CDK deployment code, pipeline and handler are covered.

**[📜Documentation](https://ran-isenberg.github.io/aws-serverless-cron-template/)** | **[Blogs website](https://www.ranthebuilder.cloud)**
> **Contact details | ran.isenberg@ranthebuilder.cloud**


## **The Problem**




## **The Solution**

This project aims to reduce cognitive load and answer these questions for you by providing a skeleton Python Serverless service template that implements best practices for AWS Lambda, Serverless CI/CD, and AWS CDK in one template project.

### Serverless Service - The Cron Job Service



### **Features**

- Python Serverless service with a recommended file structure.
- CDK infrastructure with infrastructure tests and security tests.
- CI/CD pipelines based on Github actions that deploys to AWS with python linters, static code analysis, complexity checks and style formatters.
- The AWS Lambda handler embodies Serverless best practices and has all the bells and whistles for a proper production ready handler.
- AWS Lambda handler uses [AWS Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/).
- Unit, integration and E2E tests.


## CDK Deployment
The CDK code create an API GW with a path of /api/orders which triggers the lambda on 'POST' requests.

The AWS Lambda handler uses a Lambda layer optimization which takes all the packages under the [packages] section in the Pipfile and downloads them in via a Docker instance.

This allows you to package any custom dependencies you might have, just add them to the Pipfile under the [packages] section.

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
Head over to the complete project documentation pages at GitHub pages at [https://ran-isenberg.github.io/aws-lambda-handler-cookbook](https://ran-isenberg.github.io/aws-lambda-handler-cookbook/)

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
