Changelog
=========

1.7.1 (unreleased)
------------------

Added:

- Prepare review docker image #4243
  [slindner]

- Bulk actions (transfer, transition and delete) for items in Folders and Collections. #2693 and #3460
  [pbauer]

  - New view for collections "Docpool view with bulk actions"
  - New view dpdocument_transition_form for bulk transitions
  - New view folder_delete for bulk content delete
  - New toggle-all checkbox for listings with actions
  - Add debug logger to myView
  - Remove/replace python scripts and cpt's transferDPDocument.cpy, migrateELANTransfers.py, isSender.py, getTupleForTransfer.py, dpdocument_transfer_form.cpt
  - Pass portal_type of real context to macros and hide some actions in collections (see also #2693)

Changed:

- Switched to new CI runner & docker #4158
  [slindner]

- Simplify generated title for REI-reports. #4224
  [kprobst]

Fixed:

- Fix adding events without journals. #4267
  [pbauer]

- Reimplement scenario selection; more efficient and robust adding, closing and removing. #4324
  [tlotze]

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
