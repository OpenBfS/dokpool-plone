# Development install

# Install & Setup

```
$ mkvirtualenv dokpool-plone
$ cd dokpool-plone/Plone
$ pip installl -r requirements.txt
$ sudo apt install libpq-dev
$ sudo apt-get install libsqlite3-dev
$ sudo apt install postgresql
$ bin/buildout -c local-develop.cfg
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
$ createdb elan -U elan

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

dual-use branches
-----------------

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

Das Webpack Theme ist nur in einer Plone Seite aktiv die "dokpool" heißt. Die URL muss
also so aussehen: "http://localhost:8080/dokpool/"
Beim Aufruf von "/@@docpool_setup" wird das neue Theme wird automatisch aktiviert.

#### Entwicklung mit Webpack

Das Theme befindet sich in `Plone/src/docpool.theme/docpool/theme/webpack_resources`,
erst müssen die dort die Javascript Abhängigkeiten installiert werden:

.. code-block:: bash

    $ cd Plone/src/docpool.theme/docpool/theme/webpack_resources
    $ npm install

Jetzt kann hot-reloading verwendet werden, bedeutet bei Änderungen im
`webpack_resources` Verzeichnis wird automatisch die Seite neu geladen.
Die Plone Instanz muss dazu laufen:

.. code-block:: bash

    $ bin/instance fg
    $ cd Plone/src/docpool.theme/docpool/theme/webpack_resources
    $ npm run watch

#### Neue Bundle-Files erstellen

Damit aktualisierte CSS/JS Dateien direkt von Plone ausgeliefert werden, müssen diese
erstellt und eingecheckt werden:

.. code-block:: bash

    $ bin/instance fg
    $ cd Plone/src/docpool.theme/docpool/theme/webpack_resources
    # Wir löschen die alten bundle Dateien, so behalten wir keine unnötigen Dateien
    $ rm -Rf theme
    # Wir lassen das theme Verzeichnis mit allen bundle Dateien neu erstellen.
    $ npm run build
    # Wir commiten die Source Dateien extra, damit ist der Merge-Request besser zu lesen
    $ git add src/
    $ git commit -m "Update xyz styling"
    $ Jetzt commiten wir die Webpack bundle Dateien
    $ git add theme/
    $ git commit -m "Update bundle files"

Haben sich CSS/LESS/JS Dateien von Plone oder in unseren bestehenden
Resources (z.B in: `Plone/src/docpool.theme/docpool/theme/diazo_resources/static`)
geändert,  muss das `.plone` Verzeichins in `webpack_resources` gelöscht werden. Beim
nächsten `npm run build/watch` werden diese Dateien dann neu von Plone geladen.

#### Bundle-Files rebase / update

Oft entstehen durch ein rebase conflicts an den bundle files. Kurze Anleitung wie damit umzugehen ist:

1. git checkout develop
2. git pull
3. git checkout own_local_branch
4. git rebase develop

Wenn es bei den bundle files ein conflict gibt:

git add src/docpool.theme/docpool/theme/webpack_resources/theme/
git rebase --continue

ggf. wiederholen.

Nach dem rebase die bundle files nochmal neu erstellen, siehe "Neu Bundle-files erstellen"
