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

Sources
---------

Publicly available repo:


## Preparing and Configuration

##### Install and Prepare DokPool 

- see https://github.com/OpenBfS/dokpool-plone

##### Install elan.journal

- install the package via "*Site Setup*" > "*Addons*"

###### create journal and group (1)

- in your *docpool/<name>/esd*: 

  - add a new Content Item of *Journal-Type*, named "*journal1*" via the Toolbar (you can change the title of this item, later on)

- in your *docpool/<name>* User and Group Management:
  - create a group (*group1*) which should make use of the Journal
  - add the (existing) role "Journal1 Editor" to *group1*

- in *docpool/<name>/esd/journal1/@@sharing*:
   - deselect "*Inherit permissions from higher levels*"
   - grant "*can view*", "*can edit*", "*can add*" to *group1* and to *Administrators*, *Administrators (<name>)*, *Content Administrators (<name>)* 


###### create journal and group (2)

- if needed, same procedure for *journal2*, *group2*


##### Working with elan.journal

Users which are members of *group1/group2* will be able to access *journal1/journal2* (or the given title) via the Overview-Portlet from the main screen.
In their User Actions, there will be a menu item "*Add Journal1 Entry / Add Journal2 Entry*".
For other users the journal will not be visible.

##### Known Issues

coming soon

 

 

 
