import pathlib
import subprocess


domain = "docpool.base"
locale_path = pathlib.Path(__file__).parent
pot = locale_path / f"{domain}.pot"
target_path = locale_path.parent
i18ndude = "i18ndude"
msgattrib = "msgattrib"

# ignore node_modules files resulting in errors
excludes = '"*.html *json-schema*.xml"'


def rebuild_pot():
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


def update_lang(lang, lc_messages_path):
    po = lc_messages_path / f"{domain}.po"
    if not lc_messages_path.is_dir():
        lc_messages_path.mkdir()
        subprocess.call(
            ["msginit", f"--locale={lang}", f"--input={pot}", f"--output={po}"]
        )

    subprocess.call([i18ndude, "sync", "--pot", pot, po])
    subprocess.call([msgattrib, "--no-wrap", "--add-location=file", "-o", po, po])


def update_locale():
    rebuild_pot()
    for path in locale_path.iterdir():
        if path.name == "__pycache__":
            continue
        if not path.is_dir():
            continue
        lc_messages_path = path / "LC_MESSAGES"
        update_lang(path.name, lc_messages_path)
