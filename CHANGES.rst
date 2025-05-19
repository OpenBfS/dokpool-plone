Changelog
=========

2.1.0 (unreleased)
------------------

Changed:

- Improve event archiving by using a form and preventing triggering it multiple times. (#5998)
  [pbauer]


Fixed:

- Use overrides.zcml to register custom importers in docpool.distribution to fix ConfigurationConflictError. (#6056)
  [pbauer]


Added:

- Show number of entries in event-picker, archive-listing and event-listing. (#5759)
  [pbauer]

- i18n structure for Romania. (#6020)
  [slindner]


Technical:

- Upgrade to Plone 6.0.15. (#4892)
  [pbauer]


2.0.1 (2025-03-31)
------------------

Changed:

- Improve ux of dpdocument_transfer_form and activateFilter by enabling click on label.
  [pbauer]

- Redirect RODOS-App to /projections. (#2609)
  [pbauer]


Fixed:

- Fix issue that content in archives was not displayed in collections. (#5948)
  [pbauer]

- Prevent anonymous calls to setActiveApp. (#5938)
  [pbauer]

- Reduce odds for ConflictErrors: Avoid writing member data that didn't
  actually change. (#5983)
  [tlotze]

- Reintroduce monkey patch to avoid storing login times. (#5983)
  [tlotze]

- Fix viewing/editing the fields of a DPDocument in /dexterity-types/DPDocument/@@fields. (#5970)
  [pbauer]

- Fix editing reireports without MStIDs. (#5969)
  [pbauer]

- In Docpool/App menu, compute targets prior to redirect. (#5997)
  [tlotze]

- Fix dashboardcollection and recent-portlet when not inside a dokpool. (#5977)
  [pbauer]

- Use here instead of context in content-rule. (#5982)
  [pbauer]

- Keep view of listing after a single transition. (#5984)
  [pbauer]

- Prevent setting invalid app as memberproperties. (#5996)
  [pbauer]

- In Docpool/App menu, compute target urls prior to redirect and fix linking back from archive. (#5997)
  [pbauer]

- Hide usermanagement-action from local admins without admin-role on dokpool. (#2609)
  [pbauer]

- Update translation (#5785)
  [pbauer]

- Add some space before pdflink (#5942)
  [pbauer]

Added:

- Add marker interface ISkipAutomaticTransferMarker to allow skipping automatc transfers for
  certain containers (#5982)
  [pbauer]

- Add scenario_ids to serialized DPDocument (#5999)
  [pbauer]


Technical:

- Fix issue with setuptools and plone.autoinclude (#5963)
  [pbauer]

- Add alias for forgotten (not uninstalled) browserlayer of contentimport.
  [pbauer]


2.0.0 (2025-01-31)
------------------

This is a major release with many breaking changes and refactorings.
The following list only contains the major changes.

- Python 3 Migration and Upgrade to Plone 6. (#4345, #4824)
  Updating a existing installation requires the data to be moved to a new instance using exportimport.
  See #4345 for links to all subtasks.
  [pbauer, slindner, tlotze]

- Cleanup packages structure. (#4076)
  Remove docpool.caching and move code to docpool.base.
  Remove docpool.video.
  Remove docpool.dashboard and move code to docpool.base.
  Make etag module of docpool.base pluggable and move elan-specifics to docpool.elan.
  Remove docpool.policy.
  Remove elan.policy and move code and dependecies to docpool.config.
  Remove docpool.localbehavior and move code to docpool.base.
  Remove docpool.menu and move code to docpool.base.browser.viewlets.
  Remove docpool.transfers and move code to docpool.base.
  Remove docpool.example.
  Remove elan.sitrep.
  Remove docpool.event and move code to docpool.elan.
  Remove docpool.users and move code to docpool.base.users.
  Remove elan.esd and move code to docpool.elan.
  Remove elan.theme and move code to docpool.theme.
  [pbauer, tlotze]

- Drop special ELAN-DB and use of SQLAlchemy and Elixir. Remove package docpool.dbaccess. (#3954)
  [lotze]

- Reimplement Theme based on Plone 6 and use webpack. (#4826)
  [slindner]

- Rewrite Navigation for Plone 6. (#4825)
  [tlotze]

- Fix inheritance of instance-classes. Stop inheriting from Item and Document since they clash with Container. Drop unused interface IExtendable. (#4851)
  [pbauer]

- Refactor FlexibleView and migrate templates rendered by it to BrowserViews. (#4840)
  [pbauer]

- Remove all skin-templates and -scripts and replace with browser views. (#4831, #5467)
  [tlotze, pbauer]

- Refactor archiving and snapshot of events. (#4870)
  [pbauer]

- Refactor transfers. (#4833, #5653)
  [tlotze]

- Upgrade faceted-navigation to Plone 6 and Python 3. (#4943)
  [slindner]

- Switch to pip/uv install based on cookieplone and deploy with docker containers. (#4629, #4780, #5488, #5562, #5608)
  [pbauer, slindner]

- Implement dokpool in IMIS3 stack. (#5484)
  [slindner]

- Refactor integration and changes to discussion/commenting. (#5043, #5518)
  [pbauer]

- In navigation portlet show number of items that will be visible in a folder or collection. (#4858, #5898)
  [pbauer]

- Refactor local behaviors. (#5432, #5565)
  [tlotze, pbauer]

- Refactor the control of visibility of app-specific content. (#5434)
  [pbauer]

- For better test-content remove docpool_setup and add distribution in new package docpool.distribution. (#5681)
  [pbauer]

- Refactor redirect on frontpage. (#5450)
  [pbauer]

- Remove wsapi4plone and wsapi4elan and replace with custom restapi endpoints. (#4626)
  [pbauer]

- Refactor indexes to prevent empty indexes on clear&rebuild. (#5700, #5565)
  [pbauer]

- Switch event-selection for users and documents from id to uuid. (#5546, #5745, #5260, #5044, #4379)
  [tlotze]

- Reimplement RODOS-app. (#2609)
  [pbauer]

- Add view with bulk actions for ELANDocCollections and DashboardCollections. (#4343)
  [pbauer]

- Remove dependency on collective.geo and openlayers. Use WKT fields for now. (#3663)
  [pbauer]

- Improve performance. (#4481)
  [pbauer, tlotze]

- Fix design for content below an inaccessible navigation-root. (#5447)
  [pbauer]

- Add view @@json for admins that serializes content using restapi. (#5551)
  [pbauer]


1.9.9 (2024-11-11)
------------------

Technical:

- Added docker stack configuration
  [jbuermeyer,slindner]

- Added dependency collective.relationshelpers
  [pbauer]

- remove logger for member properties (#4325)
  [tlotze]


Fixed:

- Improve performance (#5742)
  - Cache expensive computation that used to cause very long-running requests after editing an ELANDocType.
    [tlotze]
  - Do not use the very slow python-script isArchive when calculating the categories
    [pbauer]
  - Replace slow back_references with faster api from relationhelpers
    [pbauer]


1.9.8 (2024-06-20)
------------------

Technical:

- Update journal print styling
  [pbauer]

- Update bundle files
  [slindner]

- revert logging of wsapi calls (#4626)
  [kprobst]


1.9.7 (2024-05-06)
------------------

Changed:

- Prevent leaking local behaviors of parent to newly created object (#5565)
  [pbauer]

- Fix docpool_setup
  [pbauer]

Technical:

- Log all wsapi calls to find out what is used (#5597, #4626)
  [pbauer]


1.9.6 (2024-03-22)
------------------

Changed:

- Change originvocab for REI (#5479)
  [pbauer]

Added:

- add json view for admins for debugging (#5551)
  [pbauer]

Technical:

- upgrade postgresql to 14 in Dockerfile.pgsql to fit ubuntu:latest
  [mlechner]


1.9.5 (2023-11-27)
------------------

Fixed:

- Add upgrade-steps to fix rebuild catalog and fix intid-catalog (#5413)
  [pbauer]


1.9.4 (2023-08-01)
------------------

Changed:

- Update REI vocabularies (#5137)
  [kprobst]

- log errors for events not found in UID index (while working on #5260)
  [tlotze]

Fixed:

- Disable direct role-assignment to Users and Groups in docpools for non-managers (#4391)
  [pbauer]

- ugrade-step to update rolemappings (#4560)
  [pbauer]

- do not show journals from archived events (#4993)
  [tlotze]

- fix archiving event GNU-2022-Tyche (#5007)
  [pbauer]

- fix event selection: per docpool, distinguish events with same id (#5044)
  [tlotze]

- fix upgrade step for event selection by uid (#5044)
  [tlotze]

- fix printable version for simpleviz_inline.pt (#5045)
  [kprobst]

- fix logic for selecting folder action buttons (#5135)
  [tlotze]

- fix access to DPDocument method in #4819-related patches on all portal objects (#5150)
  [slindner]

- uniquify displayed event titles for a document that is associated with
  multiple events by the same id (e.g., partly archived) (#5260)
  [tlotze]

- Remove old REI-I Medium values (#5302)
  [slindner]

Added:

- allow infodocument as defaultpage (#4643)
  [pbauer]

Technical:

- prevent varnish from timing out event archival (#3792)
  [tlotze,kprobst]

- make authentication condition configurable for varnish (#4539)
  [tlotze]

- remove the workaround for SQLAlchemyError (#4830)
  [tlotze]

- customize varnish backend error page (#4904)
  [tlotze]

- Blob-cache should be bytes (#5096)
  [slindner]


1.9.3 (2022-10-21)
------------------

Changed:

- Limit blob-cache to 25GB (#4739)
  [slindner]

Fixed:

- Move blob-cache setting to prod cfg (#4739)
  [slindner]

- Show comments in archive. (#4819)
  [tlotze]


1.9.2 (2022-08-04)
------------------

Changed:

- Limit blob-cache to 25GB. (#4739)
  [slindner]

- Speed up archiving events, bring back combined snapshot and purge. (#4870)
  [pbauer]

- Update SampleType vocabulary and change sorting on NetworksVocabulary. (#4902)
  [kprobst]

- Adapted simpleviz templates for dtypes (visualisation of non-map+legend-attachments) (#4903)
  [kprobst]

Fixed:

- Fix varnish config to avoid mixing up user identities (#4539)
  [tlotze]


1.9.1 (2022-07-05)
------------------

Fixed:

- Fix Icon path (#4808)
  [slindner]

- Fix journal permission check (#4818)
  [pbauer]

- Run CI test in correct dir (#4823)
  [slindner]


1.9.0 (2022-05-13)
------------------

Added:

- Update to Plone 5.1.7 (#4614)
  [pbauer, slindner]

- Allow dp_school as valid main url. (#4040)
  [slindner]

- Add Makefile for bundle update. (#4653)
  [slindner]

- Add collective.impersonate. (#4598)
  [pbauer]

- Browsertest for marquee ticker (#3681)
  [slindner]


Changed:

- Adapt vocabularies for event SectorizingSampleTypes and SectorizingNetworks (#3533)
  [kprobst]

- Remove not needed js file (#4174)
  [slindner]

- Replace workflow transition icons. (#4337)
  [slindner]

- Hide event status 'closed' in forms unless event is already closed. (#4634)
  [pbauer, tlotze]

- Hide plone.belowcontenttitle.documentbyline. (#4695)
  [kprobst]

- Expand EventType history. (#4463)
  [slindner]
- Add blob cache size to production buildout (#4739)
  [slindner]

Fixed:

- Don't log login times to member properties to avoid DB hotspot. (#4325)
  [tlotze]

- Update event types: IRIX-conform tokens, rename Event to Emergency, add Routine, add translations. (#3430)
  [tlotze]

- Remove old diazo resources dir and not needed js files (#3681)
  [slindner]

- Prevent deleting folders with published content by updating dp_folder_workflow. (#4560)
  [pbauer]

- Include commenting inside dview (when viewing documents in the context of a
  collection) (#3957)
  [tlotze]

- Update REI vocabularies. (#4518)
  [kprobst]

- Catch SQLAlchemy error when querying transfers. (#4758)
  [tlotze]

- Refactor archiving of Events: Move event and journals into archive. (#4374)
  [pbauer]

- Show document workflow state in dview. (#4270)
  [tlotze]


Fixed:

- Fix missing translations in Chronologie (#3708)
  [slindner]

- Limit displayed journals to current document pool. (#4515)
  [tlotze]

- Fix errors when getting local behaviors. (#3811)
  [pbauer]

- Fix modal config for dpdocument_transfer_form. (#4570)
  [pbauer]

- Fix footer display after Plone update. (#4702)
  [slindner]

- Prevent adding journalentries to closed and archived journals. (#4374)
  [pbauer]

- Fix for folder view when there is one item more than the batch size. (#4374)
  [pbauer]


1.8.4 (2021-11-04)
------------------

Technical:

- Remove remnants of old testdata infrastructure to simplify buildout (#4405)
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

Changed:

- Switch to pipenv for bootstrap (#3956)
  [tlotze, slindner]

1.8.3 (2021-09-29)
------------------

Technical:

- Configured 4 additional instances, changed varnish timeouts (#4475)
  [slindner, tlotze, kprobst]
    - Configured 4 additional instances, changed varnish timeouts (#4475) [slindner, tlotze, kprobst]


1.8.2 (2021-08-12)
------------------

Added:

- Add js alert to confirm bulk transitions (#4396)
  [pbauer]


Changed:

- Use dview if the parent is a collection (#4392)
  [pbauer]


Fixed:

- Fix year filter - facetednavigation (#4394)
  [slindner]

- Remove unallowed value from OriginVocabulary (#4388)
  [pbauer]

- Disable broken sorting in faceted navigation results table (#4395)
  [pbauer]

- Fix no_value option in AutoritiesVocabulary (#4418)
  [pbauer]


1.8.1 (2021-07-19)
------------------

Fixed:

- Fix logic for deselecting scenarios (#4324)
  [tlotze, pbauer]


1.8.0 (2021-07-19)
------------------

Added:

- Added faceted navigation functionality in REI: facetednavigation-webpack (#2634)
  [slindner]

- Added bulk actions: bulk transfer (#2693, bulk actions in collections #3460)
  [pbauer]


Changed:

- Added Collection to allowed content types for Simplefolder (#4342)
  [pbauer]

- Require medium for REI-E reports (#4269)
  [pbauer]

- Removed milliseconds in portlet recent in ELAN
  [kprobst]


Fixed:

- Fixed unicode indexes in REI (#4084)
  [pbauer]

- Fixed creating events without journals in ELAN (#4267)
  [pbauer]

- Fixed bug in creating new DocTypes (#4266)
  [tlotze]

- Fixed sorting in REI AuthorityVocabulary (#4336)
  [pbauer]

- Deactivate checkboxes when de/selecting events (#4078)
  [tlotze]


Technical:

- Fix zcml: Drop obsolete explicit zcml-slugs. Only use those with i18n-override (#4349)
  [pbauer]


1.7.4 (2021-06-10.)
------------------

Fixed:

- Update Products.PloneHotfix20210518 and allow text/html to be displayed inline
  [pbauer]


1.7.3 (2021-05-25)
------------------

Fixed:

- Bump last weeks hotfix 20210518 to version 1.2
  [tlotze]

- Deployed on master as hotfix
  [kprobst]


1.7.2 (2021-05-22)
------------------

Fixed:

- Add Plone hotfix 20210518
  [tlotze]

- Deployed on master as hotfix
  [kprobst]


1.7.1 (2021-03-23)
------------------

Changed:

- Switched to new CI runner & docker (#4158)
  [slindner]

- Simplify generated title for REI-reports. (#4224)
  [kprobst]


1.7.0 (2021-02-12)
------------------

Added:

- Added Changelog
  [slindner]

- Add custom add-form for DPDocument to hide title-field for reireport (#4039)
  [pbauer]

- Add automatic transfer of published documents to other docpools. (#2601)
  [tlotze]


Changed:

- Close all popups on logout (#3512)
  [slindner]

- Do not display content of text files (#4038)
  [pbauer]


Fixed:

- Fix Unicode Errors in AUTHORITYS vocabulary and use ISO values (#3953)
  [slindner]

- Fix compatability mode in Internet Explorer (#3991)
  [slindner]

- Fix editing help page and move it to each docpool (#2439)
  [tlotze]

- Only use global imprint, fix actions and views for help and imprint, move
  these texts out of contentconfig folders (#4067)
  [tlotze]

- Add hotfix to fix canchangepassword (#4085)
  Deployed on master as hotfix.
  [kprobst]


Technical:

- Remove the concept and implementation of auditing (#3954)
  [tlotze]

- Remove elan.irix and all other IRIX-related code (#3954)
  [tlotze]

- Remove archetypes dependencies (#3225)
  [tlotze]
