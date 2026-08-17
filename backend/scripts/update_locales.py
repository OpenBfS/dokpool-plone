import contextlib
import pathlib
import pkg_resources
import subprocess
import sys


packages = sys.argv[1:]
languages = ["de", "en", "ro"]

i18ndude = "i18ndude"

# ignore node_modules files resulting in errors
excludes = '"*.html *json-schema*.xml"'


CONFLICT_PREFIXES = (
    '"POT-Creation-Date: ',
    '"PO-Revision-Date: ',
    '"Last-Translator: ',
)


@contextlib.contextmanager
def remove_conflicting_metadata(path):
    """Write back old po(t) file if the POT Creation Date is the only change."""
    yield
    if path.is_file():
        text = path.read_text()
        lines = [l for l in text.splitlines() if not l.startswith(CONFLICT_PREFIXES)]
        path.write_text("\n".join(lines) + "\n")


def rebuild_pot(domain, pot, target_path):
    subprocess.call([
        i18ndude,
        "rebuild-pot",
        "--pot",
        pot,
        "--exclude",
        excludes,
        "--no-line-numbers",
        "--create",
        domain,
        target_path,
    ])


def update_lang(domain, pot, locale_path, lang):
    lc_messages_path = locale_path / lang / "LC_MESSAGES"
    po = lc_messages_path / f"{domain}.po"
    if not lc_messages_path.is_dir():
        lc_messages_path.mkdir(parents=True)
        subprocess.call([
            "msginit",
            f"--locale={lang}",
            f"--input={pot}",
            f"--output={po}",
        ])

    with remove_conflicting_metadata(po):
        subprocess.call([i18ndude, "sync", "--pot", pot, po])


def update_pkg(pkg):
    try:
        locale_path = pathlib.Path(pkg_resources.resource_filename(pkg, "locales"))
    except (ModuleNotFoundError, TypeError):  # no locales directory in this package
        return

    domain = pkg
    pot = locale_path / f"{domain}.pot"
    target_path = locale_path.parent
    with remove_conflicting_metadata(pot):
        rebuild_pot(domain, pot, target_path)
    for lang in languages:
        update_lang(domain, pot, locale_path, lang)


for pkg in packages:
    update_pkg(pkg)
