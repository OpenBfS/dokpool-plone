echo ${JOB_NAME##*/}

# delete old virtualenv
if [ -d "$WORKSPACE/venv/${JOB_NAME##*/}" ]; then
        rm -R $WORKSPACE/venv/${JOB_NAME##*/}
fi
# create new virtualenv
if [ ! -d "$WORKSPACE/venv/${JOB_NAME##*/}" ]; then
        virtualenv -p $PythonBinPath $WORKSPACE/venv/${JOB_NAME##*/}
fi
echo "Using Python Version:"
python -V
echo "from:"
which python

source $WORKSPACE/venv/${JOB_NAME##*/}/bin/activate
if [ -d "Plone" ]; then
        cd Plone
        echo "Using Python Version:"
        python -V
        echo "from:"
        which python
        pip install --upgrade pip docutils
        if [ -f "requirements.txt" ]; then
                pip install -r requirements.txt
        fi
        buildout bootstrap
        printf '[buildout]\nextends =\n    buildout.cfg\n[ports]\ninstance_dev = 18082\n' >> buildout_jenkins.cfg
        if [ -f "bin/buildout" ]; then
                ./bin/buildout -v -c buildout_jenkins.cfg
        fi
fi
deactivate

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
