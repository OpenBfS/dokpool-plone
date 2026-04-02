from BTrees.OOBTree import OOBTree
from distutils.spawn import find_executable
from logging import getLogger
from pathlib import Path
from plone.app.contenttypes.interfaces import IFile
from plone.namedfile.file import NamedBlobImage
from plone.scale.scale import scaleImage
from tempfile import TemporaryDirectory
from zope.annotation import IAnnotations
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

import datetime
import subprocess
import transaction


logger = getLogger(__name__)

ANNOTATION_KEY = "docpool.preview_image"

ALLOWED = ["application/pdf"]

SCALES = [
    ("great", 1200, 65536),
    ("teaser", 600, 65536),
    ("mini", 200, 65536),
]

QUALITY = 88


class PDF2JPGSubProcess:
    """
    Convert first page of a pdf to an jpg
    """

    pdftocairo_path = find_executable("pdftocairo")

    def convert(self, input_path):
        with TemporaryDirectory(prefix="docpool") as tmpdir:
            cmd = [self.pdftocairo_path, input_path, "-singlefile", "-jpeg", Path(tmpdir) / "preview"]
            self._run_command(cmd)
            with open(Path(tmpdir) / "preview.jpg", "rb") as tmp_preview_image:
                return tmp_preview_image.read()

    def _run_command(self, cmd, env=None):
        if isinstance(cmd, str):
            cmd = cmd.split()

        cmdformatted = " ".join(map(str, cmd))
        logger.debug("Running command: %s" % cmdformatted)
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, env=env
        )
        output, error = process.communicate()
        process.stdout.close()
        process.stderr.close()
        if process.returncode != 0:
            error = """Command
%s
finished with return code
%i
and output:
%s
%s""" % (
                cmdformatted,
                process.returncode,
                output,
                error,
            )
            logger.info(error)
            raise Exception(error)
        logger.debug("Finished Running Command %s" % cmdformatted)
        return output


pdf2jpg = PDF2JPGSubProcess()
if not pdf2jpg.pdftocairo_path:
    logger.error(
        "No `pdftocairo` (from `poppler-utils`) command in your PATH. Preview generation will not work."
    )


@adapter(IFile, IObjectAddedEvent)
def generate_preview_image_on_add(obj, event=None):
    generate_preview_image(obj)


@adapter(IFile, IObjectModifiedEvent)
def generate_preview_image_on_modified(obj, event=None):
    generate_preview_image(obj)


def generate_preview_image(obj):
    """ """
    # Check if parent is DPDocument and the File has a file
    if obj.__parent__.portal_type != "DPDocument" or not obj.file:
        return

    # Check if we can generate preview from this mime_type
    mime_type = obj.file.contentType
    if mime_type not in ALLOWED:
        # We only support pdf for now
        return

    # Initialize or get existing previews
    annotations = IAnnotations(obj)
    previews = annotations.get(ANNOTATION_KEY, None)
    if previews is None or not previews.get("relative_blob_path", None):
        previews = OOBTree()
        previews["last_updated"] = None
        previews["relative_blob_path"] = None
        annotations[ANNOTATION_KEY] = previews

    if not obj.file._blob._p_oid:
        # This only works when the file was already saved!
        # TODO: Maybe use async instead.
        transaction.commit()

    connection = obj._p_jar
    connection.setstate(obj.file._blob)
    db = connection.db()
    relative_blob_path = db.storage.fshelper.layout.getBlobFilePath(
        obj.file._blob._p_oid, obj.file._blob._p_serial
    )

    # Check that there is no preview already
    if previews["relative_blob_path"] == relative_blob_path:
        # File is unchanged, keep existing preview
        logger.debug("Keep existing previews of %s", obj.absolute_url())
        return

    # Send blob-path to subprocess to generate preview image
    blob_path = Path(db.storage.fshelper.base_dir) / Path(relative_blob_path)
    data = pdf2jpg.convert(blob_path)
    mode = "scale"
    parameters = {"quality": QUALITY}
    for scalename, height, width in SCALES:
        image, _, _ = scaleImage(data, mode=mode, height=height, width=width, **parameters)
        blob = NamedBlobImage(image, contentType="image/jpg", filename="preview.jpg")
        previews[scalename] = blob

    # Save previews as annotation
    previews["relative_blob_path"] = relative_blob_path
    previews["last_updated"] = datetime.datetime.now().timestamp()
    logger.info("Generated previews for %s", obj.absolute_url())
