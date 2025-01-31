# Dokpool

**Dokpool** is a CMS based on Plone6, a website developed for handling documents in multiple contexts, using several editorial roles and workflows.

- The main application for **Dokpool** is **ELAN**, an Electronic Situation Display for the management of radiological emergencies. In ELAN, the contents of a radiological emergency are recorded and made available to relevant parties in a workflow process.
- In **REI**, reports from the operators and monitoring bodies of nuclear facilities are recorded and made available to the competent authorities in accordance with the REI Directive on Emission and Immission Monitoring of Nuclear Facilities.
- Various specialist and technical documents for the routine monitoring of environmental radioactivity within the framework of the "Integrated Measurement and Information System" IMIS are managed in **IMIS DokSys**
- The **RODOS** application manages calculations from the prognosis and decision support model RODOS ("Realtime Online Decision Support System") of the future environmental contamination and the expected doses to the affected population in a radiological emergency

#### Contact

Bundesamt für Strahlenschutz / General Office for Radiation Protection\
Willy-Brandt-Strasse 5\
38226 Salzgitter\
info@bfs.de

#### License

**Dokpool** including ELAN and most of its components are published using the [GNU GPL v>=3](http://www.gnu.org/licenses/gpl-3.0) license.

#### Sources

Publicly available repo:

```
git clone https://github.com/OpenBfS/dokpool-plone.git
```

#### Latest Release

2.0.0

## Building

### Running Dokpool in standalone docker container

For rapid, simple testing/demonstration
-> See Docker (https://www.docker.com) for further information on this Container technology.

#### (1) Build image (dokpool-plone6-standalone)

```
git checkout 2.0.0
cd backend
docker build --force-rm=true -t dokpool-plone6-standalone -f Dockerfile .
```

#### (2) Start docker container (dokpool_plone6_standalone_8081)

##### (2a) to use with demo data, changes will not be saved locally if docker container is removed:

```
cd backend
docker run --restart=always --name dokpool_plone6_standalone_8081 --publish 8081:8080 dokpool-plone6-standalone
```

##### (2b) with external data-volume, changes will be saved in backend/data even if docker container is removed

```
cd backend
mkdir data # if not yet existing
docker run --restart=always --name dokpool_plone6_standalone_8081 --publish 8081:8080 --volume $(pwd)/data:/data dokpool-plone6-standalone
```

In case you want to interact with the running container, use e.g.

```
$ docker exec -it dokpool_plone6_standalone_8081 /bin/bash
```

### Running Dokpool with docker-compose stack

coming soon

## Configuration in Webbrowser: Create a Dokpool site with demo content

On the intro screen (create a site) of http://localhost:8081,
click on „_Dokpool Site with demo content"_ -> Create

Fill in the form:

- Path Identifier: dokpool
- Title: Dokpool Test
- Site Description: Test with docpooldemo
- Site Logo: ()
- Language: (if English, the menues and system notifications will be in English, demo content is only available in German at the moment)
- Timezone
- **Check „Create Example Content“**

The site will be available via

- http://localhost:8081 under „Existing Sites“ (docpooldemo)
- http://localhost:8081/\<Path Identifier> (e.g. http://localhost:8081/dokpool)

If Dokpool was started according to (2b), changes will be saved in backend/data even if the docker container is removed.

## Development

coming soon

## More Information

Accounts to log into Dokpool/ELAN using a webbrowser, e.g. Firefox.

#### Admin-Login:

Username: `admin`
Password: `admin`

### Users and Passwords

Additionally, there are some more power users with default passwords

at DokPool-Level (http://localhost:8081/docpool/@@usergroup-userprefs)

- `elanmanager` / `admin`
- `dpmanager` / `admin`
- `elanadmin` / `admin`
- `edpadmin` / `admin`

and at ELAN-Level (http://localhost:8081/docpool/`<name>`/@@usergroup-userprefs)

- `<name>_elanadmin` / `admin` (E.g. `bund_elanadmin`)
- `<name>_dpadmin` / `admin`

Also, there are user in the Bund/Hessen Dokpool with access to Elan, Doksys and REI and in the ContentSender group:

- `user1` / `dp_user1` (for the bund docpool)
- `user2` / `dp_user2` (for the hessen docpool)

**Default passwords should be changed before Dokpool goes to production mode: Login as specific user and change your own password in the user menu**
