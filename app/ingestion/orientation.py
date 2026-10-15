import logging
import cv2
import pytesseract

logger = logging.getLogger(__name__)

def detect_orientation(image) -> int:
    """
    Returns a rotation angle to apply: 0, 90, 180, or 270.
    OSD is best-effort because it can fail on pages with too little text.
    """
    try:
        osd = pytesseract.image_to_osd(image)
        rotation = 0
        for line in osd.splitlines():
            if line.startswith("Rotate:"):
                rotation = int(line.split(":")[1].strip())
                break
        return rotation if rotation in (0, 90, 180, 270) else 0
    except Exception as exc:
        logger.warning("Orientation detection failed: %s", exc)
        return 0

def rotate_image(image, angle: int):
    if angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    if angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    if angle == 270:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image

