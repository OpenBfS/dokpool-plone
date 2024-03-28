import pathlib
import pkg_resources
import subprocess
import sys


packages = sys.argv[1:]
languages = ["de", "en"]

i18ndude = "i18ndude"
msgattrib = "msgattrib"

# ignore node_modules files resulting in errors
excludes = '"*.html *json-schema*.xml"'


def rebuild_pot(domain, pot, target_path):
    subprocess.call(
        [
            i18ndude,
            "rebuild-pot",
            "--pot",
            pot,
            "--exclude",
            excludes,
            "--create",
            domain,
            target_path,
        ]
    )
    subprocess.call([msgattrib, "--no-wrap", "--add-location=file", "-o", pot, pot])


def update_lang(domain, pot, locale_path, lang):
    lc_messages_path = locale_path / lang / "LC_MESSAGES"
    po = lc_messages_path / f"{domain}.po"
    if not lc_messages_path.is_dir():
        lc_messages_path.mkdir(parents=True)
        subprocess.call(
            ["msginit", f"--locale={lang}", f"--input={pot}", f"--output={po}"]
        )

    subprocess.call([i18ndude, "sync", "--pot", pot, po])
    subprocess.call([msgattrib, "--no-wrap", "--add-location=file", "-o", po, po])


def update_pkg(pkg):
    locale_path = pathlib.Path(pkg_resources.resource_filename(pkg, "locales"))
    domain = pkg
    pot = locale_path / f"{domain}.pot"
    target_path = locale_path.parent
    rebuild_pot(domain, pot, target_path)
    for lang in languages:
        update_lang(domain, pot, locale_path, lang)


for pkg in packages:
    update_pkg(pkg)
