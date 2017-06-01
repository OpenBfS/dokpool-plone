# Dokpool
**Dokpool** is a CMS based on Plone 5, a website developed for handling documents in multiple contexts, using several editorial roles and workflows. The main application for **Dokpool** is ELAN5, an Electronic Situation Display for the emergency management. 

#### Contact

Bundesamt für Strahlenschutz / General Office for Radiation Protection
SW2 Notfallschutz, Zentralstelle des Bundes (ZdB)
Willy-Brandt-Strasse 5
38226 Salzgitter
info@bfs.de

#### License

**Dokpool** including ELAN5 and most of its components are published using the [GNU GPL v>=3](http://www.gnu.org/licenses/gpl-3.0) license.
See `LICENSE` for more details.

Sources
---------
Publicly available repo:
```
git clone https://github.com/OpenBfS/dokpool-plone.git
```

## Building

(1) For *rapid simple testing/demonstrations* we provide Dockerfiles in `./Docker` .
*---> See Docker (https://www.docker.com) for further information on this Container technology.*

(2) If you want to run **Dokpool** *in a current Linux Distribution* there are several ways. 
&nbsp; &nbsp; &nbsp; (a) run **Dokpool** *as simple test installation* using ZODB/SQLite Backend 
&nbsp; &nbsp; &nbsp; (b) or run it *in a production environment* using PostgreSQL as Backend.
&nbsp; &nbsp; &nbsp; Using Varnish/Supervisor, **Dokpool** can be configured to run in a *multi instance mode* as well. 
*---> See several `*.cfg` files in `./Plone` to be used with buildout.*


### Prerequisites:
- If you want to start from scratch, just go on. 
- If you want to use a preconfigured Dokpool, you need a zodb-Backup (created with plonebackup) of a zodb or adequate Dumps of a PostgreSQL. --> *See various Dockerfiles in* `./Docker` *that take care of this.* 
*Containers using zodb/sqlite as backend run standalone using sqlite- and zope-Databases but are not recommended for production use!* 
- For production use a PostgreSQL-DB backend is recommended.


### (1) Build using Docker Containers:
FIXME
```sh
$ docker build --force-rm=true -t elan5/standalone -f Dockerfile.standalone .
```
or for Oracle Linux
```sh
$ docker build --force-rm=true -t elan5/standalone -f Dockerfile.oel7 .
```
#### Run: 
```sh
$ docker run --name elan5_standalone -dp 18081:8081 elan5/standalone:latest
```
Your running **Dokpool** is available on port 18081 on your host machine (http://localhost:18081).

In case you want to interact with the running container, use e.g.
```sh
$ docker exec -it elan5_standalone "/bin/bash"
```

### (2) Build your own standalone Dokpool/ELAN5 on a current Linux Distribution
To build **Dokpool** on a current Linux Distribution you simply have to clone the repository, run a few commands from command line interface and get it running. 
**Dokpool** refuses to run as root. Add a system account (e.g. elan) which can be used to run Dokpool.

#### Requirements:
- system account (e.g. `elan`) which can be used to run Dokpool.
- Git (to clone the Repo).
- Python2.7 
- Libraries: 
```sh
$ apt-get install python libxml2-dev libxslt-dev libssl-dev libsasl2-dev libldap2-dev libffi-dev python-virtualenv tar libjpeg-turbo8-dev python-dev gcc make g++ ghostscript libav-tools
```

#### (a) Dokpool with sqlite:
#### Build:
```sh
$ git clone https://github.com/OpenBfS/dokpool-plone.git
$ cd dokpool-plone/Plone
$ export ELANENGINE=sqlite:////tmp/elan5db
$ python ./bootstrap.py -v "2.5.2"
$ ./bin/buildout -vc buildout.cfg
```

#### Rebuild:

```sh
$ cd dokpool-plone/Plone
$ export ELANENGINE=sqlite:////tmp/elan5db
$ python ./bootstrap.py -v "2.5.2"
$ ./bin/buildout -Nvc buildout.cfg
```

#### Run / Start instance:

```sh
$ cd dokpool-plone/Plone
$ export ELANENGINE=sqlite:////tmp/elan5db
$ ./bin/instance fg
```

#### Stop instance:

```sh
$ CTRL-C
```

#### (b) Dokpool with PostgreSQL
#### Installation and Preparation of Postgres:
**Install Postgres Server and Client:**
```sh
$ apt-get install postgresql-server-dev postgresql-client
```
**Establish Access to Postgres Configuration File**
Check if `pg_config` can be called from the system prompt
```sh
$ pg_config
```
if not (answer: `command not found`): 
add path to postgres config file to environment variable:
- locate the file `pg_config` in your Postgres Directory on the server, e.g. in `/usr/pgsql-9.5/bin`
- the path to this file mus be added to the `PATH` variable of user `elan`
```sh  
(if logged in as elan:) 
$ PATH=$PATH:/usr/pgsql-9.5/bin
$ export PATH
```
**Create the Needed Databases and Database Users:**
```sh  
#Create database zodb (user zodbuser, password zodb)
$ sudo -u postgres createdb -0 zodbuser zodb 
#Create database elan (user elan, password elan)
$ sudo -u postgres createdb -0 elan elan
```

#### Build:
```sh
$ git clone https://github.com/OpenBfS/dokpool-plone.git
$ cd dokpool-plone/Plone
$ python ./bootstrap.py -v "2.5.2"
$ buildout -vc relstorage.cfg
```

#### Rebuild:

```sh
$ cd dokpool-plone/Plone
$ python ./bootstrap.py -v "2.5.2"
$ ./bin/buildout -Nvc relstorage.cfg
```

#### Run / Start Application:

```sh
$ cd dokpool-plone/Plone
$ ./bin/supervisord
```

#### Shutdown / Stop Application:

```sh
$ cd dokpool-plone/Plone
$ ./bin/supervisorctl shutdown all
```

## Backup and Restore Standalone Instances

```sh
$ cd dokpool-plone/Plone
$ ./bin/plonebackup-full
# backups will be stored in
# dokpool-plone/Plone/var/plonebackups
$ ./bin/plonebackup-restore
```

## Access to the Application
#### URLs:
instance / instance1 (if started via supervisord): &nbsp; http://localhost:8081
instance2 (- if started via supervisord): &nbsp; http://localhost:8082
varnish (- if started via supervisord): &nbsp; http://localhost:8100
supervisor: &nbsp; http://localhost:9001

#### Admin-Login:
Username: `admin`
Password: `istrator`

## Preparing Dokpool
#### Create a Plone Site, Install Policy
- open your application (http://localhost:8081)
- login as `admin` 
- create a Plone Site (via button), e.g. `docpool` *(choose name, title, language)*
- go to "*Site Setup*" (http://localhost:8081/docpool/@@overview-controlpanel)
- go to "*Addons*" (http://localhost:8081/docpool/@@prefs_install_products_form) and install `elan.policy` and  `wsapi4elancore`
- go to "*Resource Registries*" (http://localhost:8081/docpool/@@resourceregistry-controlpanel) and compile the Bundles `docpool`, `docpool-anon`, `docpool-config`, `docpool-dashboard`, `docpool-menu`, `docpool-nonadmin` and `elan-sitrep`
- Then you can open your website with http://localhost:8081/docpool

#### Create a Docpool
- logon to your Plone Site as `admin`
- Add a docpool via Plone Tool Bar / menu item "Add" 
- give a `<name>` and a `<prefix>` and select the available applications (e.g. ELAN)
- after that, you can logon to the docpool with `<prefix>_elanadmin` / `admin`

## Known Issues
coming soon

## Mailing Lists
coming soon

## Contributing
coming soon

## More Information

#### Users and Passwords

There are several users and passwords that should not be mixed up:

- The password of the **system user** "`elan`" - just needed for  login/logout the system.
There is a **system account** "`postgres`" as well,  running the PostgreSQL database cluster. 
*Usually you do not have to set a password for this account.*

- The passwords of the **database accounts** "`elan`" and "`zodbuser`" -  needed by `Dokpool` to get access to the two databases in the PostgreSQL database cluster. User "`elan`" should have "`elan`" as password and  "`zodbuser`" should have "`zodb`".
*PostgreSQL has its own user management independent from the operating system.*

- The accounts from the **Dokpool application** *(totally independent from the system- or database accounts.)* These are the accounts to log into Dokpool/ELAN using a webbrowser, e.g. Firefox. 
The initial default account for this is Username: `admin` PW: `istrator`

Additionally there are some more power users with default passwords 

at DokPool-Level (http://localhost:8081/docpool@@usergroup-userprefs)
 
- `elanmanager / admin`
- `dpmanager / admin`
- `elanadmin / admin`
- `dpadmin /admin`

and at ELAN-Level (http://localhost:8081/docpool/<name>@@usergroup-userprefs)
 
- `<name>_elanadmin`
- `<name>_dpadmin`

**Default passwords should be changed before Dokpool goes to production mode**
-	login as specific user and change your own password in the user menu

#### Language
Basically, Plone is supporting different languages which can be set when creating a Plone Site. 

**Configuration of  language-specific *portal properties*, *document types* and *navigation items* of `Dokpool` in external files:**
For English, German and Romanian, there are already configuration files that can be copied to standard configuration files before buildout is run.

portal properties:
```
dokpool-plone/Plone/src/elan.policy/elan/policy/profiles/default/properties.xml
dokpool-plone/Plone/src/elan.policy/elan/policy/profiles/default/properties_en.xml
dokpool-plone/Plone/src/elan.policy/elan/policy/profiles/default/properties_de.xml
dokpool-plone/Plone/src/elan.policy/elan/policy/profiles/default/properties_ro.xml
```
```
$ cp dokpool-plone/Plone/src/elan.policy/elan/policy/profiles/default/properties_de.xml dokpool-plone/Plone/src/elan.policy/elan/policy/profiles/default/properties.xml
```
configuration (general):
```
dokpool-plone/Plone/src/docpool.config/docpool/config/general/base.py
dokpool-plone/Plone/src/docpool.config/docpool/config/general/base_en.py
dokpool-plone/Plone/src/docpool.config/docpool/config/general/base_de.py
dokpool-plone/Plone/src/docpool.config/docpool/config/general/base_ro.py
dokpool-plone/Plone/src/docpool.config/docpool/config/general/elan.py
dokpool-plone/Plone/src/docpool.config/docpool/config/general/elan_en.py
dokpool-plone/Plone/src/docpool.config/docpool/config/general/elan_de.py
dokpool-plone/Plone/src/docpool.config/docpool/config/general/elan_ro.py
```
```
$ cp dokpool-plone/Plone/src/docpool.config/docpool/config/general/base_de.py dokpool-plone/Plone/src/docpool.config/docpool/config/general/base.py
$ dokpool-plone/Plone/src/docpool.config/docpool/config/general/elan_de.py dokpool-plone/Plone/src/docpool.config/docpool/config/general/elan.py
```
configuration (local):
```
dokpool-plone/Plone/src/docpool.config/docpool/config/local/base.py
dokpool-plone/Plone/src/docpool.config/docpool/config/local/base_en.py
dokpool-plone/Plone/src/docpool.config/docpool/config/local/base_de.py
dokpool-plone/Plone/src/docpool.config/docpool/config/local/base_ro.py
dokpool-plone/Plone/src/docpool.config/docpool/config/local/elan.py
dokpool-plone/Plone/src/docpool.config/docpool/config/local/elan_en.py
dokpool-plone/Plone/src/docpool.config/docpool/config/local/elan_de.py
dokpool-plone/Plone/src/docpool.config/docpool/config/local/elan_ro.py
```
```
$ cp dokpool-plone/Plone/src/docpool.config/docpool/config/local/base_de.py dokpool-plone/Plone/src/docpool.config/docpool/config/local/base.py
$ dokpool-plone/Plone/src/docpool.config/docpool/config/local/elan_de.py dokpool-plone/Plone/src/docpool.config/docpool/config/local/elan.py
```

**Translation of text strings**
Plone i18n uses the standard gettext system for internationalization. In every product, there are special .po-files in which the text strings used in the application can be translated, e.g.
```
dokpool-plone/Plone/src/docpool.base/docpool/base/locales/de/LC_MESSAGES/docpool.base.po
```
The relevant translations will be used if
- the plone site has been created in the target language
- the browser language has been switched to the target language
- the target language is configured in the relevant sections of `buildout.cfg`, e.g.
```
[i18nize_docpoolbase]
recipe = collective.recipe.template
input = ${buildout:directory}/buildout.d/i18nize.in
output = ${buildout:bin-directory}/i18nize_docpoolbase
mode = 775
dollar = $
domain = docpool.base
packagepath = ${buildout:directory}/src/docpool.base/docpool/base
languages = en de
```
#### Browser based Configuration
Further documentation on browser based configuration of the Plone Site and `Dokpool` (*e.g. scenarios, dashboard, modular situation report*) will soon be available on our ELAN Demo website.
