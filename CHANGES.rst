Changelog
=========

1.7.4
-----

Added:


Changed:


Fixed:

- Update Products.PloneHotfix20210518 and allow text/html to be displayed inline
[pbauer]


Removed:


Technical:



1.7.3
-----

Added:


Changed:


Fixed:

- Bump last weeks hotfix 20210518 to version 1.2
  [tlotze]
  Deployed on master as hotfix
  [kprobst]


Removed:


Technical:



1.7.2
-----

Added:


Changed:


Fixed:

- Add Plone hotfix 20210518
  [tlotze]
  Deployed on master as hotfix
  [kprobst]


Removed:


Technical:


1.7.1
-----

Added:


Changed:

- Switched to new CI runner & docker #4158
  [slindner]

- Simplify generated title for REI-reports. #4224
  [kprobst]

Fixed:


Removed:


Technical:


1.7.0 (12.02.2021)
------------------

Added:

- Added Changelog
  [slindner]

- Add custom add-form for DPDocument to hide title-field for reireport #4039
  [pbauer]

- Add automatic transfer of published documents to other docpools. #2601
  [tlotze]

Changed:

- Close all popups on logout #3512
  [slindner]

- Do not display content of text files #4038
  [pbauer]


Fixed:

- Fix Unicode Errors in AUTHORITYS vocabulary and use ISO values #3953
  [slindner]

- Fix compatability mode in Internet Explorer #3991
  [slindner]

- Fix editing help page and move it to each docpool #2439
  [tlotze]

- Only use global imprint, fix actions and views for help and imprint, move
  these texts out of contentconfig folders #4067
  [tlotze]

- Add hotfix to fix canchangepassword #4085
  Deployed on master as hotfix.
  [kprobst]


Removed:


Technical:

- Remove the concept and implementation of auditing #3954
  [tlotze]

- Remove elan.irix and all other IRIX-related code #3954
  [tlotze]

- Remove archetypes dependencies #3225
  [tlotze]
