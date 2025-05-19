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


POT_PREFIX = '"POT-Creation-Date: '


@contextlib.contextmanager
def reset_pot_creation_date(path):
    """Write back old po(t) file if the POT Creation Date is the only change."""
    if not path.is_file():
        yield
        return
    old_text = path.read_text()
    old_lines = [l for l in old_text.splitlines() if not l.startswith(POT_PREFIX)]
    yield
    if path.is_file():
        new_text = path.read_text()
        new_lines = [l for l in new_text.splitlines() if not l.startswith(POT_PREFIX)]
        if old_lines == new_lines:
            path.write_text(old_text)


def rebuild_pot(domain, pot, target_path):
    subprocess.call(
        [
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
        ]
    )


def update_lang(domain, pot, locale_path, lang):
    lc_messages_path = locale_path / lang / "LC_MESSAGES"
    po = lc_messages_path / f"{domain}.po"
    if not lc_messages_path.is_dir():
        lc_messages_path.mkdir(parents=True)
        subprocess.call(
            [
                "msginit",
                f"--locale={lang}",
                f"--input={pot}",
                f"--output={po}",
            ]
        )

    with reset_pot_creation_date(po):
        subprocess.call([i18ndude, "sync", "--pot", pot, po])


def update_pkg(pkg):
    try:
        locale_path = pathlib.Path(pkg_resources.resource_filename(pkg, "locales"))
    except TypeError:  # no locales directory in this package
        return

    domain = pkg
    pot = locale_path / f"{domain}.pot"
    target_path = locale_path.parent
    with reset_pot_creation_date(pot):
        rebuild_pot(domain, pot, target_path)
    for lang in languages:
        update_lang(domain, pot, locale_path, lang)


for pkg in packages:
    update_pkg(pkg)
