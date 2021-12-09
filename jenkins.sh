echo ${JOB_NAME##*/}

export VIRTUAL_ENV="$WORKSPACE/venv/${JOB_NAME##*/}"

# delete old virtualenv
if [ -d "$VIRTUAL_ENV" ]; then
        rm -R $VIRTUAL_ENV
fi
# create new virtualenv
if [ ! -d "$VIRTUAL_ENV" ]; then
        virtualenv -p $PythonBinPath $VIRTUAL_ENV
fi
echo "Using Python Version:"
python -V
echo "from:"
which python

if [ -d "Plone" ]; then
        cd Plone
        echo "Using Python Version:"
        python -V
        echo "from:"
        which python
        pipenv install
        printf '[buildout]\nextends =\n    buildout.cfg\n[ports]\ninstance_dev = 18082\n' >> buildout_jenkins.cfg
        pipenv run buildout -v -c buildout_jenkins.cfg
fi

cd $WORKSPACE

if [ "$GitTag" == "develop" ]; then
  git archive --prefix=dokpool/ -o $WORKSPACE/dokpool-SNAPSHOT.tgz HEAD
else
  myVersion="${GitTag##*/}"
  if [[ "$GitTag" == refs* ]]; then
    echo "seems to be a tagname"
    git archive --prefix=dokpool/ -o $WORKSPACE/dokpool-$myVersion.tgz $GitTag
  else
    echo "seems to be a branchname"
    git archive --prefix=dokpool/ -o $WORKSPACE/dokpool-$myVersion.tgz origin/$myVersion
  fi
fi

cp $WORKSPACE/dokpool-*.tgz /home/koala/repo/dokpool/
for i in dokpool-*.tgz; do md5sum $i > /home/koala/repo/dokpool/$i.md5; done
