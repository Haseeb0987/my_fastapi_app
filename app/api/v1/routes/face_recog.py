import json
import os
import io
from datetime import datetime
import face_recognition
import numpy as np
from fastapi import APIRouter, UploadFile, File
from PIL import Image, ImageOps

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API is running!!!"}


def process_image_get_encoding(upload_file: UploadFile):
    """
    Convert UploadFile → Encodings (list of floats)
    Safely handles corrupted images, rotation, PNG transparency, etc.
    Returns: encoding list OR None
    """

    try:
        # Read file bytes
        file_bytes = upload_file.file.read()
        if not file_bytes:
            return None

        # Open using PIL
        pil_img = Image.open(io.BytesIO(file_bytes))

        # Fix rotation
        pil_img = ImageOps.exif_transpose(pil_img)

        # Ensure RGB
        pil_img = pil_img.convert("RGB")

        # Convert to numpy
        np_img = np.array(pil_img).astype("uint8")
        np_img = np.ascontiguousarray(np_img)

        # Face encoding
        enc = face_recognition.face_encodings(np_img)

        if len(enc) == 0:
            return None  # No face found

        return enc[0].tolist()  # return 128-d encoding

    except Exception as e:
        print("Image Processing Error:", e)
        return None


@router.post("/saveStudentFaceEncodings/{stu_regno}")
async def save_student_face_encodings(
    stu_regno: str,
    frontImg1: UploadFile = File(None),
    frontImg2: UploadFile = File(None),
    leftImg: UploadFile = File(None),
    rightImg: UploadFile = File(None),
):
    # Ensure folder exists
    os.makedirs("app/assets/Students", exist_ok=True)

    # Images dictionary for looping
    image_dict = {
        "frontImg1": frontImg1,
        "frontImg2": frontImg2,
        "leftImg": leftImg,
        "rightImg": rightImg
    }

    # Final dictionary to save encodings or null
    encodings_output = {}

    for img_key, img_file in image_dict.items():
        if img_file is None:
            encodings_output[img_key] = None
            continue

        try:
            # Save backup file
            save_path = f"app/assets/Students/{stu_regno}_{img_key}.jpg"
            contents = await img_file.read()
            with open(save_path, "wb") as f:
                f.write(contents)

            # Reset pointer for processing
            img_file.file.seek(0)

            # Process image
            encoding = process_image_get_encoding(img_file)

            encodings_output[img_key] = encoding  # encoding or None

        except Exception as e:
            print(f"Processing error for {img_key}: {e}")
            encodings_output[img_key] = None

    # JSON file path
    json_file_path = "app/assets/student_encodings.json"
    os.makedirs("app/assets", exist_ok=True)

    # Load old file if exists
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, "r") as f:
                data = json.load(f)
        except:
            data = {}
    else:
        data = {}

    # Update entry
    data[stu_regno] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "encodings": encodings_output
    }

    # Save final JSON
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "status": "success",
        "reg_no": stu_regno,
        "message": "Encodings saved successfully.",
        "encodings_found": sum(1 for v in encodings_output.values() if v is not None)
    }
