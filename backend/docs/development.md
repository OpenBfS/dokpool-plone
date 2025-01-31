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
