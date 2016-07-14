/* Sicherheitsabfrage vor dem Loeschen von Datensaetzen. */
function sicherheitsabfrage(){
    checkboxen = jQuery('.dbadmin .gridtable .check input:checked');
    anzahl = checkboxen.length;
    if (anzahl > 0) {
        text = escape('Wollen Sie ' + anzahl + ' Objekt(e) ' + unescape('l%F6schen%3F'));
        return confirm(unescape(text));
    }
    return false;
}

function einfachesicherheitsabfrage(){
    text = escape('Wollen Sie den Datensatz wirklich ' + unescape('l%F6schen%3F'));
    return confirm(unescape(text));
}

function securitycheck(){
    checkboxen = jQuery('.dbadmin .gridtable .check input:checked');
    anzahl = checkboxen.length;
    if (anzahl > 0) {
        text = escape('Do you want to delete ' + anzahl + ' object(s) ?');
        return confirm(unescape(text));
    }
    return false;
}

function simplesecuritycheck(){
    text = escape('Do you really want to delete this object?');
    return confirm(unescape(text));
}