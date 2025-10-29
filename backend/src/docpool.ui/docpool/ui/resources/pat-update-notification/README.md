# pat-update-notification

## Code style

The release process based on release-it includes automatic changelog generation via conventional-commit, commitlint and a pre-commit hook to check the commit message format.
Please check the [code style guide](https://github.com/Patternslib/Patterns/blob/master/docs/developer/styleguide.md#commits-messages) for the commit specification!

## Release

The created package has a Patternslib enabled release workflow.
By default the package lives in the `@patternslib` scope on npm.

You might want to change these paramters to fit your release process and accessible npm scopes.
If you believe you need access to the npm `@patternslib` scope create an [Issue on Patterns](https://github.com/Patternslib/Patterns/issues).

## Documentation

This is simple pattern project bootstrap template.

Usage:

    ./create.sh PROJECTNAME

This will create a directory within this directory with the name `pat-PROJECTNAME`.
You can use it for developing a new pattern.
