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
