# Release Dokumentation

Ticket template: https://redmine-koala.bfs.de/issues/4384

## Prepare Code for Deployment

1. Create release branch `release/1.x.x` from current `develop`
1. Test release branch
1. Upgrade version to 1.x.x (edit `Plone/src/docpool.base/setup.py`)
1. Merge `release/1.x.x` into master
1. Create tag `1.x.x `on `master`
1. Upgrade dev-version on `develop`

## Deploy

1. Checkout tag `1.x.x` (= master)
1. Run buildout
1. Restart server and instances

## Run Relevant Upgrade Steps

- Use ZMI (`/portal_setup/manage_upgrades`)
