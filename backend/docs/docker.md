# Docker

WIP Docker howto

## Docker Image build

Image muss so mit relativem Pfad vom Projekt-Root gebaut werden:
(Sonst werden die Porjektfiles nicht gemountet)

.. code-block:: bash

    $ docker build --force-rm=true -t bfs/dokpool5standalone -f ./Docker/ubuntu16/Dockerfile.standalone .',

## How to debug build failures

Tritt ein Fehler beim build auf z.B:

.. code-block:: bash

    Step 7/17 : RUN mkdir -p /opt/bfs/dokpool
     ---> Using cache
     ---> a3c2914e01c1
    Step 8/17 : ADD . /opt/bfs/dokpool/
     ---> d3a8dda9383b
    Step 9/17 : WORKDIR /opt/bfs/dokpool/Plone
     ---> Running in b58d6a3b151d
    Removing intermediate container b58d6a3b151d
     ---> a0a359e2065c
    Step 10/17 : RUN cd /opt/bfs/dokpool/Plone && pip2 install --upgrade pip && pip install --upgrade docutils && pip install -r requirements.txt
     ---> Running in bccdcdc4a569
    Collecting pip
      Downloading https://files.pythonhosted.org/packages/27/79/8a850fe3496446ff0d584327ae44e7500daf6764ca1a382d2d02789accf7/pip-20.3.4-py2.py3-none-any.whl (1.5MB)
    Installing collected packages: pip
      Found existing installation: pip 9.0.1
        Not uninstalling pip at /usr/lib/python2.7/dist-packages, outside environment /usr
    Successfully installed pip-20.3.4
    DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. pip 21.0 will drop support for Python 2.7 in January 2021. More details about Python 2 support in pip can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support pip 21.0 will remove support for this functionality.
    Collecting docutils
      Downloading docutils-0.16-py2.py3-none-any.whl (548 kB)
    Installing collected packages: docutils
      Attempting uninstall: docutils
        Found existing installation: docutils 0.14
    ERROR: Cannot uninstall 'docutils'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.
    Removing intermediate container bccdcdc4a569

Nun kann man in ein bestehenden Teil des Containers springen und den letzten Befehl ausführen:

.. code-block:: bash

$ docker run -it a0a359e2065c bash
