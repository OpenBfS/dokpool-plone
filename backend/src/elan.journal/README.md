# elan.journal

**elan.journal**

is an add-on product for [ELAN5 (Dokpool)](https://github.com/OpenBfS/dokpool-plone)

It adds a Journal content type to the site. A journal is a blog post which is intended to provide a rolling textual coverage of an ongoing event. Code adapted from [collective.liveblog](https://github.com/collective/collective.liveblog)

#### Contact

Bundesamt für Strahlenschutz / General Office for Radiation Protection
SW2 Notfallschutz, Zentralstelle des Bundes (ZdB)
Willy-Brandt-Strasse 5
38226 Salzgitter
info@bfs.de

#### License

**Dokpool** including ELAN5 and most of its components are published using the [GNU GPL v>=3](http://www.gnu.org/licenses/gpl-3.0) license.

## Sources

Publicly available repo:

## Preparing and Configuration

##### Install and Prepare DokPool

- see https://github.com/OpenBfS/dokpool-plone

##### Install elan.journal

- install the package via "_Site Setup_" > "_Addons_"

###### create journal and group (1)

- in your _docpool/<name>/esd_:
  - add a new Content Item of _Journal-Type_, named "_journal1_" via the Toolbar (you can change the title of this item, later on)

- in your _docpool/<name>_ User and Group Management:
  - create a group (_group1_) which should make use of the Journal
  - add the (existing) role "Journal1 Editor" to _group1_

- in _docpool/<name>/esd/journal1/@@sharing_:
  - deselect "_Inherit permissions from higher levels_"
  - grant "_can view_", "_can edit_", "_can add_" to _group1_ and to _Administrators_, _Administrators (<name>)_, _Content Administrators (<name>)_

###### create journal and group (2)

- if needed, same procedure for _journal2_, _group2_

##### Working with elan.journal

Users which are members of _group1/group2_ will be able to access _journal1/journal2_ (or the given title) via the Overview-Portlet from the main screen.
In their User Actions, there will be a menu item "_Add Journal1 Entry / Add Journal2 Entry_".
For other users the journal will not be visible.

##### Known Issues

coming soon
