To run the popcrn frontend, run 'python SimpleHTTPServer <port>' on the root directory, and navigate to 'localhost:<port>/templates/'
to view the index page.

The server/harvester requires a lot of pre-processing and setup, so if you need
assistance getting it up, please feel free to shoot me an email at sahil_prasad@brown.edu.

VIRTUALENV

Ensure that you have 'pip' installed, and run 'pip install virtualenv' to install
the virtualn environment package. This ensures that all dependencies that are necessary
to run our application do not impact other applications on the system.

Then, in the parent directory of 'popcrn', run 'virtualenv pvenv' to set up the virtual environment.
To activate it, run 'source pvenv/bin/activate'. You are now in the environment.

DEPENDENCES

To install all dependencies, 'cd' into 'popcrn', ensure that you are in the location of
'setup.py' and run 'python setup.py develop'. This will install all dependencies on your
virtual environment. NOTE: this may take a while.

MYSQL

This project utilizes a local MySQL database in order to run. To set MySQL up, please
make sure that Homebrew is installed, and run 'brew install mysql' to set it up.

Afterwards, run 'mysql -u root -p', providing necessary credentials, and type the following
in order to set up the database:

'create database popcrn default charset utf8mb4 collate utf8mb4_unicode_ci;'

After this, exit the shell with 'exit'.

DATABASE SCHEMA SETUP

We use a library called 'alembic' to handle database migrations, so to initialize the schema
of the database, run 'alembic upgrade head'.

RABBITMQ

Popcrn utilizes an asynchronous messaging service, RabbitMQ, that runs the twitter harvesting
tasks that we need to populate the database properly.

To install, run 'brew install rabbitmq'.

TWITTER

We utilize the Twitter API through environment variables, meaning that we store our keys and tokens
in the environment to make it possible for others to use our application. We have provided our keys here
for the convenience of the TA that is grading this.

Please set the following:

TWITTER_ACCESS_SECRET -> Y6nNsr6vyvtjW55sLmWnNCmhdzkwDZldPc91kkIMTDiJa
TWITTER_ACCESS_TOKEN -> 3397682950-pm7PFS5To0a8pCu2pHoxjdvKw0jQBeTNf0PTsWg
TWITTER_CONSUMER_SECRET -> 1hE99ZCErIeHCXOELh94hkSpbxccPG5qXvOPQTTPoKcOhTjkB4
TWITTER_CONSUMER_KEY -> Nb5VVbYsLamUxE7be7t2erb46

TO RUN!!!!

After all of the setup to this program, there are three things that must be done
before running the server:

1. run rabbit mq (usually, by running 'rabbitmq-server' from another terminal)
2. open up another shell, activate the virtual environment, navigate to the root of the project,
and run 'celery worker --maxtasksperchild=2 -A popcrn.ingestion.tasks -c2 -lINFO'
3. from another shell that has the virtual environment activated as necessary,
  run 'pserve development.ini' in order to actually run the server.

1 (explained) -- this script initializes the RabbitMQ service, making it possible for
applications utilizing the appropriate protocols to enqueue tasks to be run asynchronously
from their executing threads.
2 (explained) Celery is a library for Python that provides asynchronous task processing, scheduling,
and managing functionality, allowing us to queue our harvest tasks with RabbitMQ, and handle them
accordingly with the logic that is present within our task code. Celery operates by instantiating
workers that handle jobs, and we specify that the max tasks (or "jobs") that our worker can handle
is 2, to reduce the load on the system and ensure that if something goes wrong, we can stop the harvester
before many bad things happen to the data.
3 (explained) 'pserve' is the command that serves the application that we created using the Pyramid
framework, and the INI file that we specified provides settings and configuration details that are
necessary to it.

POST-SETUP

Now, the server is listening on port 6543. If a request is made to localhost:6543/?topic=whatevertopicyouwant,
the harvester will queue up a task to harvest tasks and populate the database. At the time of writing, the application
is not fully integrated with the frontend, meaning that the data visualized is not the data that is sent. However, we
believe that this is a small matter, as it only involves the hooking up static context files to the server and passing in
required variables. We ran out of time or else we would have had a fully-communicating application. Please refer to the instructions
on how to run and view the front end at the beginning of this document for more information about that.
