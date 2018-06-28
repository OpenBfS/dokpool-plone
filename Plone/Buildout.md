Erfordert aktuelle Versionen von
* virtualenv
* pip


```sh
virtualenv ../pyenv
source ../pyenv/bin/activate
pip install -r requirements.txt
buildout bootstrap
./bin/buildout -vc buildout.cfg
./bin/instance fg
deactivate
```