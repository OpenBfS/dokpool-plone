from BTrees.OOBTree import OOBTree
from distutils.spawn import find_executable
from logging import getLogger
from pathlib import Path
from plone.app.contenttypes.interfaces import IFile
from plone.namedfile.file import NamedBlobImage
from tempfile import TemporaryDirectory
from zope.annotation import IAnnotations
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

import datetime
import subprocess


logger = getLogger(__name__)

ANNOTATION_KEY = "docpool.preview_image"

ALLOWED = ["application/pdf"]


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
        logger.info("Running command: %s" % cmdformatted)
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
        logger.info("Finished Running Command %s" % cmdformatted)
        return output


pdf2jpg = PDF2JPGSubProcess()
if not pdf2jpg.pdftocairo_path:
    logger.error(
        "No `pdftocairo` (from `poppler-utils`) command in your PATH. Preview generation will not work."
    )
if not pdf2jpg.pdfinfo_path:
    logger.error(
        "No `pdfinfo` (from `poppler-utils`) command in your PATH. Preview generation will not work."
    )


@adapter(IFile, IObjectAddedEvent)
def generate_preview_image_on_add(obj, event=None):
    generate_preview_image(obj)


@adapter(IFile, IObjectModifiedEvent)
def generate_preview_image_on_modified(obj, event=None):
    generate_preview_image(obj)


def generate_preview_image(obj):
    """ """
    # TODO: Do we want to exportimport previews or generate then on the fly?
    # if IImportingMarker.providedBy(getRequest()):
    #     return

    # 1. Check if parent is DPDocument and obj has a file
    if obj.__parent__.portal_type != "DPDocument":
        return
    if not obj.file:
        return

    annotations = IAnnotations(obj)
    previews = annotations.get(ANNOTATION_KEY, None)
    if previews is None:
        previews = OOBTree()
        previews["last_updated"] = None
        previews["relative_blob_path"] = None
        annotations[ANNOTATION_KEY] = previews

    mime_type = obj.file.contentType

    # 2. Check if we can generate preview from this mime_type
    if mime_type not in ALLOWED:
        # We only support pdf for now
        return

    # 3. Check that there is no preview already
    connection = obj._p_jar
    connection.setstate(obj.file._blob)
    db = connection.db()
    relative_blob_path = db.storage.fshelper.layout.getBlobFilePath(
        obj.file._blob._p_oid, obj.file._blob._p_serial
    )

    if previews["relative_blob_path"] == relative_blob_path:
        # File is unchanged, keep existing preview
        return

    # 4. Send blob-path to too to generate preview image
    blob_path = Path(db.storage.fshelper.base_dir) / Path(relative_blob_path)
    data = pdf2jpg.convert(blob_path)
    image = NamedBlobImage(data, contentType="image/jpg", filename="preview.jpg")

    # TODO: Generate different scales
    img_200 = image
    img_600 = image
    img_1200 = image

    previews["1200"] = img_1200
    previews["600"] = img_600
    previews["200"] = img_200
    previews["relative_blob_path"] = relative_blob_path
    previews["last_updated"] = datetime.datetime.now().timestamp()
