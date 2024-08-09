# Development install

# Install & Setup

```
$ sudo apt install libsqlite3-dev libpq-dev postgresql pipenv
$ cd dokpool-plone/Plone
$ pipenv install
$ pipenv shell
$ buildout -c local-develop.cfg
```

## Start with filestorage and demo content

```
$ bin/instance fg
```

Create a new vanilla Plone-Site (without any addons activated). Access http://localhost:8080/Plone/@@docpool_setup and start the demo creation process.

## With a production backup database

On Debian you maybe need "sudo -u postgres" in front of all commands.

```
DB und user löschen (z.B. beim Einspielen von prod backup - siehe unten):
$ dropdb zodb
$ dropuser zodbuser

User und DB anlegen:
$ createuser --createdb zodbuser
# On Mac OS ($ createdb zodb -U zodbuser)
$ createdb -O zodbuser zodb
$ sudo -u postgres psql
$ alter user zodbuser with encrypted password 'zodbuser';

DB restore:
$ pg_restore -d zodb dokpool_20190920-1210.backup
```

Do the same for elan db:

```
Create elan DB
$ dropdb elan
$ dropuser elan

User und DB anlegen:
$ createuser --createdb elan
# On Mac OS ($ createdb elan -U elan)
$ createdb elan -O elan
$ sudo -u postgres psql
$ alter user elan with encrypted password 'elan';

DB restore:
$ pg_restore -d elan produktiv_elan_20201009.backup
```

Create an admin user since we don't know the production admin's credentials:

```
$ ./bin/instance_relstorage adduser rescue rescue
```

Instance should start up with Postgres DB und Relstorage:

```
$ bin/instance_relstorage fg
```

## Convert production backup database to filestorage

Alten Blob-Cache löschen:

```
$ rm -rf blobs/*
$ rm blobs/.layout
```

Diesen Code als var/convert_to_datafs.conf speichern:

```
<relstorage source>
    shared-blob-dir false
    blob-dir ./blobs
    <postgresql>
        dsn dbname=zodb user=zodbuser host=localhost password=zodbuser port=5432
    </postgresql>
</relstorage>

<blobstorage destination>
  blob-dir ./var/blobstorage
  # FileStorage database
  <filestorage>
    path ./var/filestorage/Data.fs
  </filestorage>
</blobstorage>
```

Die Postgres DB kann danach mit diesem Befehl in eine Data.fs mit blobstorage
umgewandelt werden:

```
$ bin/zodbconvert var/convert_to_datafs.conf
```

# Development

## Repositories

The primary code repository is hosted by Starzel: https://git.starzel.de/bfs/dokpool

A secondary repository at https://redmine-koala.bfs.de/scm/git/dokpool is
exclusively meant as a means to allow production deployment from inside the
BfS infrastructure. The primary repository is configured to push-mirror its
content to the BfS one (that is, by a gitlab configuration rather than, e.g.,
a cron job). This is a one-way road, so there's no guarantee about anything
pushed directly to the secondary repository by accident.

## Branches

### master

The branch with the code that is released on production. We release tags that exists on this branch, e.g. 2.1.0

### develop

The branch which is currently developed. Used for demos or test-deployments.

### tag (ex. 1.5.0)

The branch in which a certain version is being prepared before deployment.

### ticket_xxxx_some_task

A feature-branch, cut from develop which will be merged back to develop as soon as a feature is done.

Example:

.. code-block:: bash

    # Update develop
    $ git checkout develop
    $ git pull origin develop
    # Create new branch
    $ git checkout -b ticket_123_fix_was
    # Do changes and commit if needed
    $ git commit -a -m 'Fix something (#123)'
    # Push the branch to gitlab
    $ git push origin ticket_123_fix_was
    # Gitlab reports back with a merge request url
    # Visit the url and create a new merge request
    # Wait for a successful CI run and assign to reviewer

## dual-use branches

When a feature is meant to be used in develop and in release/xxx we need to first create a branch from develop and later create another from release/xxx. The changes in the first branch will be cherry-picked into the second branch.

Example:

.. code-block:: bash

    git checkout develop
    git checkout -b ticket_123_fix_was

make some changes

.. code-block:: bash

    git commit -a -m 'Fix something (#123)'
    git push

create pull-request

.. code-block:: bash

    git checkout release/2.1.0
    git checkout -b ticket_123_fix_was_for_release210
    git cherry-pick --no-commit xxxxxxx (the hash of the commit with 'Fix something (#123)')

maybe make more changes to make the original changes compatible with the release-branch

.. code-block:: bash

    git commit -a -m 'Fix something (#123) for release/2.1.0'
    git push

create pull-request

### Theme Entwicklung

#### Install nvm - node - npm

Zur Installation von npm/node wird NVM empfohlen: [Installationsanleitung](https://github.com/nvm-sh/nvm#installing-and-updating)

Dieses Webpack Theme ist getestet mit diesen Versionen, die stable Version von Node sollte funktionieren:

.. code-block:: bash

    [develop]$ node -v
    v12.14.1
    [develop]$ npm -v
    6.13.4

Yarn (eine Alternative zu npm) funktioniert nicht mit diesem Webpack Theme.

#### Installation in Plone

#### Entwicklung mit Webpack

Javascript Abhängigkeiten installieren:

.. code-block:: bash

    $ cd Plone
    $ npm install

Instanzen starten:

.. code-block:: bash

    $ bin/instance fg
    # In einem anderen Terminal
    $ npm run watch

### Review App

Durch ein Push auf den "review" branch kann eine komplette Installation zum Review angstossen werden.

.. code-block:: bash

    # Delete existing review branch (lokal & remote)
    $ git branch -d review
    $ git push origin --delete review
    # In den Branch wechseln der zum Review bereit gestellt werden soll. Z.B:
    $ git checkout ticket-2634-facetednavigation-webpack
    # Diesen Branch in review kopieren:
    $ git checkout -b review
    $ git push origin review

In Gitlab den MR richtig benamen: "Draft: Review App von ticket-2634-facetednavigation-webpack"
Das Label "review" setzen.

### Test with own (prod) database

    $ mkdir bfs-test && cd bfs-test
    $ mkdir data && cd data
    $ tar xf <path to db>/db.tar -C .
    $ mv blobs blobstorage
    $ find blobstorage -type f -name "*.blob" -print -exec chmod 666 {} \;
    $ cd ..
    $ docker login git.starzel.de:5050 -u <gitlab-login> -p <password>
    $ docker pull git.starzel.de:5050/bfs/dokpool:python3
    $ docker run --publish 8080:8080 -v $(pwd)/data:/data git.starzel.de:5050/bfs/dokpool:python3
    # Open http://localhost:8080

### Export Docker Image

Da die Entwicklungsversion z.Z. noch von internen Git-Repositories abhängt, ist ein Test mit dem fertigen Docker-Image nötig.
Hier wird der Export und Import des Docker-Images beschrieben:

    $ docker login git.starzel.de:5050 -u <gitlab-login> -p <password>
    $ docker pull git.starzel.de:5050/bfs/dokpool:python3
    # Save the docker image to a tar file
    $ docker save -o dokpool.tar git.starzel.de:5050/bfs/dokpool:python3
    # Copy the tar to another machine and import
    $ docker load -i dokpool.tar
    $ docker run --publish 8080:8080 git.starzel.de:5050/bfs/dokpool:python3
    # Open http://localhost:8080

