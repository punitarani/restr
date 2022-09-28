restr
=====


About
-----

*restr* is a RESTful Web Application Mapping, Testing and Fuzzing Tool.


Development
-----------

**Clone the repository**:

``git clone git://github.com/punitarani/restr.git``


**Install the dependencies**:

``poetry install``

Activate virtual environment:

``poetry shell``


**Run the tests**:

``python -m pytest tests -vv``

With coverage:

``coverage run -m pytest tests -vv``


**Run the formatter and linter**:

``black $(git ls-files '*.py')``

``pylint $(git ls-files '*.py')``

=====
