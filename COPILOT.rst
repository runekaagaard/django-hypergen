Se also Makefile.

Installation::

    copilot app init hypergen --domain=hypergen.it DOES NOT WORK buuuuuh!
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

Fix --domain WILL NOT WORK buuuuuuuuuh
======================================

Here is manual on how to add custom domain for deployed application manually:

a. Issue SSL certificate via ACM for your your.route53.managed.domain
b. Bind this certificate to ALB HTTPS listener in EC2→Load Balancers (you will need to create HTTPS listener if you didn't use --domain option to copilot app init)
c. In that same listener add one more rule “send all requests from your.route53.managed.domain to the same target group”
d. Create A-record for this domain in Route53 and point into app load balancer (with empty subdomain if it points to domain itself). ALB can be chosen from dropdown list.
    
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
