# Conventions


## Technical Changelog

* File `CHANGES.txt` in the main repository.
* English
* Changes are categorized: Added/Changed/Fixed/Deprecated/Removed
* Each entry ends with a Ticketnummer (or commit-hash if there is no ticket)
* We do not track recurring changes like updating translations or the bundle.


An Example for the technical Changelog:

```
1.2.1 (unreleased)
------------------

Added:

- Meeting minutes can be sent as drafts. #1627
  [pbauer, gomez]

- 055ee463

Changed:

- Set start and end date for meetings as required. #1751
  [pbauer]

Fixed:

- Demo meetings now have an end date. #1746
  [pbauer]

- Only display "Aufgabe löschen" when there are tasks  zum löschen vorhanden sind. #1686
  [jesse]


1.2 (2017-11-08)
----------------

Added:

- AD/LDAP sync can now also fetch portrait images. #1435
  [name]

- The site search now looks in to more user profile fields: (person_title, department, address, ...) #1429
  [name]

- Added an optional parameter in the search utility query method that allows the backend to perform unsecure searches.
  [name]
```


## Feature-branches

* Feature-branches need to have a entry in CHANGES.txt
* PRs to such branches do not need that


## Pull-Requests

* Usefull short title that describes the change
* The Description can be more explicit
* needs the ticket number like #1234. Gitlab turns this into a link.


## Commit message

* Please write useful commit messages!
* Always ends with ticket number if there is one.
