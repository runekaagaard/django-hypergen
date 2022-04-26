Use global python, not a python in a venv.

Setup::

    sudo python3 -m pip install --upgrade build twine

Release::

    python3 -m twine upload dist/* --verbose
    python3 -m build
    
