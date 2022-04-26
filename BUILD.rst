::

    sudo python3 -m pip install --upgrade build twine
    python3 -m build
    python3 -m twine upload dist/* --verbose
