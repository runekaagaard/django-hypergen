# django-hypergen

Hypergen is a framework on top of Django that makes it easy to create responsive web pages without javascript.

# Running the examples

    git clone git@github.com:runekaagaard/django-hypergen.git
    cd django-hypergen/
    virtualenv -p python3.9 venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r examples/requirements.txt
    cd examples
    python manage.py migrate
    python manage.py runserver
    # open
    #     http://127.0.0.1:8000/todomvc/
    # or
    #     http://127.0.0.1:8000/inputs/

# Developing

## Backend

1. Format all python code with yapf
2. Run all tests with: `pytest --tb=native -x -vvvv test_all.py`

## Frontend

    sudo yarn global add parcel-bundler
    # or
    sudo npm install -g parcel-bundler
    cd hypergen/static/hypergen
    parcel watch -o hypergen.min.js -d . hypergen.js
    
## Profiling

    rm -f /tmp/hypergen.profile && python -m cProfile -o /tmp/hypergen.profile manage.py runserver 127.0.0.1:8002
    echo -e 'sort tottime\nstats' | python3 -m pstats /tmp/hypergen.profile | less
    #
    rm -f /tmp/hypergen.profile && python -m cProfile -o /tmp/hypergen.profile manage.py inputs_profile && \
        echo -e 'sort tottime\nstats' | python3 -m pstats /tmp/hypergen.profile | less
