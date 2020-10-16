# Checklisten

* [ ] **Upgrade-Steps**: Wurde daran gedacht, für all solche Änderungen am Code, die sich auf bestehende Daten auswirken, Migrationscode in Form von Upgrade-Steps für Plone zu schreiben?
* [ ] **Changelog**: Wurde die Änderung aussagekräftig und mit Ticketnummer im Changelog erwähnt?
* [ ] **Lesbarkeit**: Wurden Coding-Konventionen erfüllt, und ist der Code möglichst selbsterklärend formuliert?
* [ ] **Docstrings**: Haben alle Code-Einheiten, deren Name oder Inhalt nicht zur Erklärung ausreicht, Dokumentation in Docstrings?
* [ ] **Dokumentation**: Wurden nicht selbsterklärende Teile der neuen Funktion und der Implementierung an erwartbarer Stelle für die jeweilige Zielgruppe dokumentiert?
* [ ] **Performance**: Wurde darauf geachtet, unnötig unperformanten Code zu vermeiden und Abwägungen zwischen Performance und anderen Zielen wie Einfachheit und Lesbarkeit zu dokumentieren? Wie wirkt sich der neue Code auf die Performance der bestehenden Anwendung aus?
* [ ] **Usability**: Ist das neue Feature so einfach wie möglich benutzbar? Wurden zu beachtende Punkte dokumentiert? Wirkt sich die Änderung auf die Benutzbarkeit der bestehenden Anwendungsteile aus?
* [ ] **Test-Coverage**: Wurde aller neue Code getestet und sichergestellt, dass die Maßzahlen für die Testabdeckung nicht sinken? Dieses Kriterium kann automatisiert per CI überpüft werden, siehe 9c).
* [ ] **Risikoeinschätzung**: Gibt es Aspekte, die nicht ausreichend prüfbar waren? Kann es sein, dass bestehende Eigenschaften der Anwendung unbemerkt beeinträchtigt wurden?
* [ ] **Technische Schulden**: Wurde die Neuentwicklung insofern abgeschlossen, als dass keine Nacharbeiten an der technischen Qualität mehr nötig sind? Sind bei der Arbeit technische Schulden an bestehendem Code aufgefallen?
* [ ] **Komplexität**: Wurde darauf geachtet, den neuen Code so einfach wie möglich zu halten? Inwiefern erhöht das neue Feature die Gesamtkomplexität der Anwendung?
* [ ] **Dependencys**: Wurden neue Abhängigkeiten möglichst vermieden, oder wurde ggf. darauf geachtet, ihren Umfang klein zu halten und möglichst verbreitete und gut gepflegte Pakete zu verwenden, die sich gut in die bestehende Softwarelandschaft einfügen?
