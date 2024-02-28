# Erweiterte Checklisten

Entwurf für Checklisten für Merge-Requests und Tickets

## Tickets

Die folgenden Vorlagen können in Redmine hineinkopiert werden.

### Bug

```
h2. Zusammenfassung

Work in progress - wird noch ausformuliert.

Beispiel: Als Benutzer xyz kann in der Anwendung xzy kein xzy angelegt werden.

h3. Umgebung, in der der Fehler aufgefallen und reproduzierbar ist

[URL]
[Code branch/revision]

h3. Schritte zur Reproduktion

h3. Erwartetes Ergebnis

h3. Aktuelles Ergebnis

h3. Technische Hinweise (optional)

h3. Stacktrace (optional)

h3. Screenshots (optional)

h3. Weitere Information und Links
```

### Feature

```
h2. Zusammenfassung

Als Redakteur, ...

Will ich ...

Um ...

h3. Abnahmekriterien

Es ist erledigt wenn ...

h3. Weitere Information und Links

h3. Technische Hinweise (optional)

```

## Merge Requests

- [ ] **Upgrade-Steps**: Wurde daran gedacht, für all solche Änderungen am Code, die sich auf bestehende Daten auswirken, Migrationscode in Form von Upgrade-Steps für Plone zu schreiben? Befinden sich die Upgrade-Steps in docpool.base?
- [ ] **Changelog**: Wurde die Änderung aussagekräftig und mit Ticketnummer im Changelog erwähnt?
- [ ] **Lesbarkeit**: Wurden Coding-Konventionen erfüllt, und ist der Code möglichst selbsterklärend formuliert?
- [ ] **Docstrings**: Haben alle Code-Einheiten, deren Name oder Inhalt nicht zur Erklärung ausreicht, Dokumentation in Docstrings?
- [ ] **Dokumentation**: Wurden nicht selbsterklärende Teile der neuen Funktion und der Implementierung an erwartbarer Stelle für die jeweilige Zielgruppe dokumentiert?
- [ ] **Performance**: Wurde darauf geachtet, unnötig unperformanten Code zu vermeiden und Abwägungen zwischen Performance und anderen Zielen wie Einfachheit und Lesbarkeit zu dokumentieren? Wie wirkt sich der neue Code auf die Performance der bestehenden Anwendung aus?
- [ ] **Usability**: Ist das neue Feature so einfach wie möglich benutzbar? Wurden zu beachtende Punkte dokumentiert? Wirkt sich die Änderung auf die Benutzbarkeit der bestehenden Anwendungsteile aus?
- [ ] **Test-Coverage**: Wurde aller neue Code getestet und sichergestellt, dass die Maßzahlen für die Testabdeckung nicht sinken? Dieses Kriterium kann automatisiert per CI überpüft werden, siehe 9c).
- [ ] **Risikoeinschätzung**: Gibt es Aspekte, die nicht ausreichend prüfbar waren? Kann es sein, dass bestehende Eigenschaften der Anwendung unbemerkt beeinträchtigt wurden?
- [ ] **Technische Schulden**: Wurde die Neuentwicklung insofern abgeschlossen, als dass keine Nacharbeiten an der technischen Qualität mehr nötig sind? Sind bei der Arbeit technische Schulden an bestehendem Code aufgefallen?
- [ ] **Komplexität**: Wurde darauf geachtet, den neuen Code so einfach wie möglich zu halten? Inwiefern erhöht das neue Feature die Gesamtkomplexität der Anwendung?
- [ ] **Dependencys**: Wurden neue Abhängigkeiten möglichst vermieden, oder wurde ggf. darauf geachtet, ihren Umfang klein zu halten und möglichst verbreitete und gut gepflegte Pakete zu verwenden, die sich gut in die bestehende Softwarelandschaft einfügen?
