Se also Makefile.

Installation::

    copilot app init hypergen --domain=hypergen.it
    copilot init -a hypergen -d Dockerfile -n hypergen-service -t "Load Balanced Web Service"
    copilot env init --name prod --profile default --app hypergen --default-config

    
Deploy new version::

    copilot deploy -n hypergen-service -e prod

Destroy and start againzzz::

    copilot app delete
    
Log in to container::

    copilot svc exec --name hypergen --env test -c /bin/bash

Show logs::

    copilot svc logs -n hypergen -e prod

Pruning after messing with the overlay2 folder::

    docker system prune --volumes -a

Redis
=====

Installation::

    cd copilot
    copilot svc init --name redis --svc-type "Backend Service" --dockerfile ./redis/Dockerfile --port 6379

Deploy::

    copilot svc deploy --name redis --env prod

Url::

    redis.prod.hypergen.local:6379
    
Urls
====

- https://coder-question.com/cq-blog/589015
- https://stackoverflow.com/questions/64627462/aws-copilot-with-django-never-finishes-deploying
- https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-aws-copilot-cli.html
- http://bearprocess.com/2021/03/26/run-django-migration-with-aws-copilot/
- https://aws.github.io/copilot-cli/docs/getting-started/first-app-tutorial/
- https://github.com/aws/copilot-cli/issues/2071
- https://aws.github.io/copilot-cli/docs/developing/domain/
- https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Copilot.html
- https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

FAQ
===

- Cancel deploy: https://githubhot.com/repo/aws/copilot-cli/issues/2544

More Cancel deploy
==================

As a temporary solution...

Don't CTRL+C to cancel the copilot command that is stuck.

To get your copilot CLI to exit as it normally would (as it does on a successful deployment) you can do the following steps in your ECS cluster. This will result in your stack being cleaned up as well and not leaving you in limbo for hours like @sanjeevtejyan said.

Go to the task definition for your service
Click the checkbox for the newest revision (the one with the number that is failing)
Actions Menu - Update Service
Set the "number of tasks" to zero
Click next until you can click "update service"
Very shortly you will see the copilot CLI and CF stack back to normal

Scratch
=======

botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
