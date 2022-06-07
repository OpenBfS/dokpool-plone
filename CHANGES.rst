Changelog
=========

1.9.1 (unreleased)
------------------

Fixed:

- Fix Icon path #4808
  [slindner]

1.9.0 (13.05.22)
------------------

Added:

- Update to Plone 5.1.7 #4614
  [pbauer, slindner]

- Allow dp_school as valid main url. #4040
  [slindner]

- Add Makefile for bundle update. #4653
  [slindner]

- Add collective.impersonate. #4598
  [pbauer]

- Browsertest for marquee ticker #3681
  [slindner]


Changed:

- Adapt vocabularies for event SectorizingSampleTypes and SectorizingNetworks #3533
  [kprobst]

- Remove not needed js file #4174
  [slindner]

- Replace workflow transition icons. #4337
  [slindner]

- Hide event status 'closed' in forms unless event is already closed. #4634
  [pbauer, tlotze]

- Hide plone.belowcontenttitle.documentbyline. #4695
  [kprobst]

- Expand EventType history. #4463
  [slindner]

- Don't log login times to member properties to avoid DB hotspot. #4325
  [tlotze]

- Update event types: IRIX-conform tokens, rename Event to Emergency, add Routine, add translations. #3430
  [tlotze]

- Remove old diazo resources dir and not needed js files #3681
  [slindner]

- Prevent deleting folders with published content by updating dp_folder_workflow. #4560
  [pbauer]

- Include commenting inside dview (when viewing documents in the context of a
  collection) #3957
  [tlotze]

- Update REI vocabularies. #4518
  [kprobst]

- Catch SQLAlchemy error when querying transfers. #4758
  [tlotze]

- Refactor archiving of Events: Move event and journals into archive. #4374
  [pbauer]

- Show document workflow state in dview. #4270
  [tlotze]


Fixed:

- Fix missing translations in Chronologie #3708
  [slindner]

- Limit displayed journals to current document pool. #4515
  [tlotze]

- Fix errors when getting local behaviors. #3811
  [pbauer]

- Fix modal config for dpdocument_transfer_form. #4570
  [pbauer]

- Fix footer display after Plone update. #4702
  [slindner]

- Prevent adding journalentries to closed and archived journals. #4374
  [pbauer]

- Fix for folder view when there is one item more than the batch size. #4374
  [pbauer]


1.8.4 (04.11.2021)
------------------

Technical:

- Remove remnants of old testdata infrastructure to simplify buildout #4405
  [tlotze]

- Update Version of plone.session (#4539)
  [tlotze]


Fixed:

- Fix initialising scenarios when adding a document w.r.t. inactive ones (#4527)
  [tlotze]

- Prevent KeyError when no DPEvent for a scenario can be found (#4504)
  [pbauer, slindner]

- Fix deleteTransferDataInDB (#4117)
  [pbauer]

- Fix UnicodeDecodeError when filtering in @@rpopup (#4507)
  [pbauer]


1.8.3 (29.09.2021)
------------------

Technical:

- Configured 4 additional instances, changed varnish timeouts #4475
  [slindner, tlotze, kprobst]
    - Configured 4 additional instances, changed varnish timeouts #4475 [slindner, tlotze, kprobst]


1.8.2 (12.08.2021)
------------------

Added:

- Add js alert to confirm bulk transitions #4396
  [pbauer]


Changed:

- Use dview if the parent is a collection #4392
  [pbauer]


Fixed:

- Fix year filter - facetednavigation #4394
  [slindner]

- Remove unallowed value from OriginVocabulary #4388
  [pbauer]

- Disable broken sorting in faceted navigation results table #4395
  [pbauer]

- Fix no_value option in AutoritiesVocabulary #4418
  [pbauer]


1.8.1 (19.07.2021)
------------------

Fixed:

- Fix logic for deselecting scenarios #4324
  [tlotze, pbauer]


1.8.0 (19.07.2021)
------------------

Added:

- Added faceted navigation functionality in REI: facetednavigation-webpack #2634
  [slindner]

- Added bulk actions: bulk transfer #2693, bulk actions in collections #3460
  [pbauer]


Changed:

- Added Collection to allowed content types for Simplefolder #4342
  [pbauer]

- Require medium for REI-E reports #4269
  [pbauer]

- Removed milliseconds in portlet recent in ELAN
  [kprobst]


Fixed:

- Fixed unicode indexes in REI #4084
  [pbauer]

- Fixed creating events without journals in ELAN #4267
  [pbauer]

- Fixed bug in creating new DocTypes #4266
  [tlotze]

- Fixed sorting in REI AuthorityVocabulary #4336
  [pbauer]

- Deactivate checkboxes when de/selecting events #4078
  [tlotze]


Technical:

- Fix zcml: Drop obsolete explicit zcml-slugs. Only use those with i18n-override #4349
  [pbauer]


1.7.4 (10.06.2021)
------------------

Fixed:

- Update Products.PloneHotfix20210518 and allow text/html to be displayed inline
  [pbauer]


1.7.3 (25.05.2021)
------------------

Fixed:

- Bump last weeks hotfix 20210518 to version 1.2
  [tlotze]

- Deployed on master as hotfix
  [kprobst]


1.7.2 (22.05.2021)
------------------

Fixed:

- Add Plone hotfix 20210518
  [tlotze]

- Deployed on master as hotfix
  [kprobst]


1.7.1 (23.03.2021)
------------------

Changed:

- Switched to new CI runner & docker #4158
  [slindner]

- Simplify generated title for REI-reports. #4224
  [kprobst]


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


Technical:

- Remove the concept and implementation of auditing #3954
  [tlotze]

- Remove elan.irix and all other IRIX-related code #3954
  [tlotze]

- Remove archetypes dependencies #3225
  [tlotze]
