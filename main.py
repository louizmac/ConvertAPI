from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image, ImageOps, UnidentifiedImageError
from io import BytesIO

app = FastAPI(
    title="ConvertAPI",
    description="A lightweight self-hosted image conversion API",
    version="1.0.0"
)

SUPPORTED_FORMATS = {
    "JPEG", "PNG", "WEBP", "BMP", "TIFF"
}

OUTPUT_FORMATS = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "bmp": "BMP",
    "tiff": "TIFF"
}

@app.get("/")
def home():
    return {
        "name": "ConvertAPI",
        "version": "1.0.0",
        "status": "online"
    }

@app.post("/api/v1/convert")
async def convert_image(
    file: UploadFile = File(...),
    output_format: str = "png"
):
    output_format = output_format.lower()

    if output_format not in OUTPUT_FORMATS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported output format"
        )

    original = await file.read()

    if len(original) > 20 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File too large"
        )

    try:
        image = Image.open(BytesIO(original))

        if image.format not in SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=415,
                detail="Unsupported input format"
            )

        image = ImageOps.exif_transpose(image)
        image.load()

        if output_format in ["jpg", "jpeg", "bmp"]:
            if image.mode not in ["RGB", "L"]:
                image = image.convert("RGB")

        output = BytesIO()

        image.save(
            output,
            format=OUTPUT_FORMATS[output_format]
        )

        output.seek(0)

        media_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp",
            "bmp": "image/bmp",
            "tiff": "image/tiff"
        }

        extension = "jpg" if output_format == "jpeg" else output_format

        return StreamingResponse(
            output,
            media_type=media_types[output_format],
            headers={
                "Content-Disposition": (
                    f'attachment; filename="converted.{extension}"'
                ),
                "X-Original-Size": str(len(original)),
                "X-Converted-Size": str(output.getbuffer().nbytes)
            }
        )

    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image"
        )