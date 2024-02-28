from io import BytesIO
from OFS.Image import Image as OFSImage
from PIL import Image
from plone.rfc822.interfaces import IPrimaryFieldInfo
from pypdf import PdfReader
from zope.annotation.interfaces import IAnnotations

import logging
import subprocess


logger = logging.getLogger("docpool.base.pdfconversion")

inch = 72.0
cm = inch / 2.54
mm = cm * 0.1

img_thumb_format = "PNG"
img_thumb_quality = 60
img_thumb_optimize = True
img_thumb_progressive = False


img_preview_format = "PNG"
img_preview_quality = 90
img_preview_optimize = True
img_preview_progressive = False


def content_type(doc):
    try:
        return IPrimaryFieldInfo(doc).value.contentType
    except (TypeError, AssertionError):
        pass


def data(doc):
    try:
        return IPrimaryFieldInfo(doc).value.data
    except (TypeError, AssertionError):
        pass


def _fixPdf(string):
    try:
        result = string + "\n%%EOF\n"
        return result
    except Exception:
        logger.error("Unable to fix pdf file.")
        return string


def pdfobj(doc):
    pdf = None
    try:
        pdf = PdfReader(BytesIO(data(doc)))
    except BaseException:
        logger.warn("Error opening pdf file, trying to fix it...")
        fixed_data = _fixPdf(data(doc))

        # try to reopen the pdf file again
        try:
            pdf = PdfReader(BytesIO(fixed_data))
        except BaseException:
            logger.warn("This pdf file cannot be fixed.")

    if pdf and pdf.is_encrypted:
        try:
            decrypt = pdf.decrypt("")
            if decrypt == 0:
                logger.warn("This pdf is password protected.")
        except BaseException:
            logger.warn("Errors while decrypting the pdf file.")

    return pdf


def pages(pdf):
    return len(pdf.pages)


def metadata(pdf):
    data = {}
    data["width"] = pdf.pages[0].mediabox.width
    data["height"] = pdf.pages[0].mediabox.height
    data["pages"] = len(pdf.pages)
    return data


def get_images(doc, page_start=0, pages=1):
    thumb_size = (128, 128)
    preview_size = (1024, 1024)

    # set up the images dict
    images = {}

    # Extracting self.pages pages
    logger.info(f"Extracting {pages:d} page screenshots")

    for page in range(page_start, page_start + pages):
        # for each page in the pdf file,
        # set up a human readable page number counter starting at 1
        page_number = page + 1
        # set up the image object ids and titles
        image_id = "%d_preview" % page_number
        image_title = "Page %d Preview" % page_number
        image_thumb_id = "%d_thumb" % page_number
        image_thumb_title = "Page %d Thumbnail" % page_number
        # create a file object to store the thumbnail and preview in
        raw_image_thumb = BytesIO()
        raw_image_preview = BytesIO()
        # run ghostscript, convert pdf page into image
        raw_image = ghostscript_transform(doc, page_number)
        # use PIL to generate thumbnail from image_result
        try:
            img_thumb = Image.open(BytesIO(raw_image))
        except OSError:
            logger.error(f"This is not an image: {raw_image}")
            break

        img_thumb.thumbnail(thumb_size, Image.ANTIALIAS)
        # save the resulting thumbnail in the file object
        img_thumb.save(
            raw_image_thumb,
            format=img_thumb_format,
            quality=img_thumb_quality,
            optimize=img_thumb_optimize,
            progressive=img_thumb_progressive,
        )
        # use PIL to generate preview from image_result
        img_preview = Image.open(BytesIO(raw_image))
        img_preview.thumbnail(preview_size, Image.ANTIALIAS)
        # save the resulting thumbnail in the file object
        img_preview.save(
            raw_image_preview,
            format=img_preview_format,
            quality=img_preview_quality,
            optimize=img_preview_optimize,
            progressive=img_preview_progressive,
        )
        # create the OFS.Image objects
        image_full_object = OFSImage(image_id, image_title, raw_image_preview)
        image_thumb_object = OFSImage(
            image_thumb_id, image_thumb_title, raw_image_thumb
        )
        # add the objects to the images dict
        images[image_id] = image_full_object
        images[image_thumb_id] = image_thumb_object
        logger.info("Thumbnail generated.")

    return images


def ghostscript_transform(doc, page_num):
    """
    ghostscript_transform takes an AT based object with an IPDF interface
    and a page number argument and converts that page number of the pdf
    file to a png image file.
    """
    first_page = f"-dFirstPage={page_num:d}"
    last_page = f"-dLastPage={page_num:d}"
    gs_cmd = [
        "gs",
        "-q",
        "-dSAFER",
        "-dBATCH",
        "-dNOPAUSE",
        "-sDEVICE=png16m",
        "-dGraphicsAlphaBits=4",
        "-dTextAlphaBits=4",
        first_page,
        last_page,
        "-r200",
        "-sOutputFile=%stdout",  # noqa
        "-",
    ]

    image_result = None
    # run the ghostscript command on the pdf file, capture the output
    # png file of the specified page number
    bufsize = -1
    gs_process = subprocess.Popen(
        gs_cmd, bufsize=bufsize, stdout=subprocess.PIPE, stdin=subprocess.PIPE
    )
    gs_process.stdin.write(data(doc))
    image_result = gs_process.communicate()[0]
    gs_process.stdin.close()
    return_code = gs_process.returncode
    if return_code == 0:
        logger.info("Ghostscript processed one page of a pdf file.")
    else:
        logger.warn(
            "Ghostscript process did not exit cleanly! "
            "Error Code: {}".format(return_code)
        )
        image_result = None
    return image_result


def remove_image_previews(doc):
    """
    This function removes the image preview annotations if a pdf file is
    removed
    """
    # remove the annotated images
    annotations = IAnnotations(doc)
    if "pdfimages" in annotations:
        del annotations["pdfimages"]
    doc.reindexObject()
    msg = f"Removed preview annotations from {doc.id:s}."
    logger.info(msg)
    return msg
