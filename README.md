<div align="center">

# ConvertAPI

<p>
  A lightweight, open-source image conversion REST API.
  <br>
  Fast, simple, and fully self-hosted.
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-REST_API-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-black?style=flat-square" alt="License">
</p>

</div>

---

## Overview

ConvertAPI is a simple, self-hosted REST API that allows developers to convert images between popular formats without relying on external services.

Images are processed locally in memory and returned directly to the client.

## Features

- Image conversion between popular formats
- Automatic input format detection
- JPEG, PNG, WebP, BMP and TIFF input support
- JPEG, PNG, WebP, BMP and TIFF output formats
- Automatic EXIF orientation correction
- Maximum upload size of 20 MiB
- No database or external API required
- Interactive API documentation
- Fully self-hosted

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/louizmac/ConvertAPI.git
cd ConvertAPI
```

**2. Install dependencies**

```bash
python3 -m pip install fastapi uvicorn pillow python-multipart
```

**3. Start the server**

```bash
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive documentation:

`http://127.0.0.1:8000/docs`

## API Reference

### Convert Image

`POST /api/v1/convert`

Upload an image and receive the converted result.

**Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| file | File | Required | Image to convert |
| output_format | String | png | Output format: jpg, jpeg, png, webp, bmp, tiff |

**Example Request**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/convert?output_format=png" \
  -F "file=@image.webp" \
  --output converted.png
```

**Python Example**

```python
import requests

url = "http://127.0.0.1:8000/api/v1/convert"

with open("image.webp", "rb") as image:
    response = requests.post(
        url,
        files={"file": image},
        params={
            "output_format": "png"
        }
    )

response.raise_for_status()

with open("converted.png", "wb") as output:
    output.write(response.content)
```

## Supported Formats

| Format | Input | Output |
|--------|-------|--------|
| JPEG | Yes | Yes |
| PNG | Yes | Yes |
| WebP | Yes | Yes |
| BMP | Yes | Yes |
| TIFF | Yes | Yes |

JPG and JPEG refer to the same image format.

## Project Structure

```text
ConvertAPI/
├── main.py
└── README.md
```

## Notes

- Conversion results depend on the original image and selected output format.
- Converted images may be larger than the original files.
- JPEG and BMP conversion may remove transparency.
- Animated images and multi-page TIFF files are not fully supported.
- The API is intended for local development and trusted environments. Additional security measures are recommended before public deployment.

## License

Distributed under the MIT License. See `LICENSE` for details.

---

<div align="center">

  <sub>Built with Python, FastAPI and Pillow.</sub>
  <br>
  <sub>Created by <a href="https://github.com/louizmac">louizmac</a></sub>

</div>
