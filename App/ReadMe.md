

To switch to debug model:

    in settings.py: 

    change 

    ``DEBUG = False``

    to 

    ``DEBUG = True``



Install all packages in requirements.txt

1. check Mongodb:

    ``sudo service mongod start``

    ``sudo service mongod start``

2. Initialize DB (first time or reset), under App/ folder:

    ``python3 ClinicMongoDB.py``

3. Under App/mysite folder:

    ``python3 manage.py runserver``
