# Photo gallery application

This codebase contains a simple photo gallery app written in Python and Django.

# Setup

To setup the basic website you will need to have the following installed:

- python3
- pip
- sqlite3

Pip is the package manager for Python.  You can install the remaining packages required for this task using pip. You will need to run the following:
To start you should create and activate a virtual environment:

- $ python -m venv env        # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
- $ source env/bin/activate   # use `env\Scripts\activate` on Windows
- $ pip install -r requirements.txt

You then need to apply the migrations by typing:

 $ python manage.py migrate

# Intialising the database

To initialise the database with some images, next run:

 $ python manage.py loaddata data_initialisation.json

You should now be able to view photos in the db.sqlite3 database.

- $ sqlite3 db.sqlite3
- sqlite> select * from photoapp_photo;

1|Gentoo penguin|A penguin with an orange beak standing next to a rock.|2025-04-25 03:05:01.090000|photos/william-warby-_A_vtMMRLWM_p6XNd5U.jpg
2|Common side-blotched lizard|A close up of a lizard on a rock.|2025-04-25 03:05:43.727000|photos/javier-patino-loira-nortqDjv7ak_lEPhTEv.jpg
3|Griffin vulture flying|A large bird flying through a blue sky.|2025-04-25 03:06:10.757000|photos/jordi-rubies-2wNkdL2oIyU_kyCE28K.jpg
4|Jaguar|A close up of a leopard near a rock.|2025-04-25 03:06:33.664000|photos/jakub-neskora-jloJvr74Fcc_7gIJy3x.jpg
5|Japanese macaque|A monkey sitting on top of a wooden post.|2025-04-25 03:06:57.615000|photos/william-warby-ndWikw_TPfc_3mpZqAq.jpg
6|Berlin|An exciting part of Berlin. This place covers so many beautiful attractions in the city. From that spot you are already on the famous Oberbaumbrücke, you can see Molecule Man, and right behind me, you can see Berlin\'s beautiful skyline with the Fern|2025-04-25 03:07:25.377000|photos/ahmed-ali-Zl7bVVMEfg_v8WYKWZ.jpg
8|Bologna|A bike parked next to a pole.|2025-04-25 03:08:25.201000|photos/ekaterina-bogdan-BKJWsGB5h1s_rKONPRJ.jpg
9|Nazare, Portugal|Nazare, Portugal|2025-04-25 03:08:55.552000|photos/damian-ochrymowicz-GZQ7tKmEd9c_IvZfS6l.jpg
10|Alcatraz Island|A close up of a green plant.|2025-04-25 03:09:23.550000|photos/dima-dallacqua-U8TAGVPFJc4_pC1RHAs.jpg

# Run the website

You can run the website by typing:

 $ python manage.py runserver

You can now browse to the url http://127.0.0.1:8000/ to view the website.

