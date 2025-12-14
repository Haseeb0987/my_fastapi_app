import json
import os
from datetime import datetime
import face_recognition
from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.get("/")
def root():
    return {"message": "API is running!!!"}


def process_image_get_encoding_from_path(image_path: str):
    """
    Load image using face_recognition loader and extract encoding.
    Returns encoding list OR None
    """

    try:
        # Load image (most stable method)
        image = face_recognition.load_image_file(image_path)

        # Extract encodings
        encodings = face_recognition.face_encodings(image)

        if not encodings:
            print(f"No face found in image: {image_path}")
            return None

        print(f"Encoding generated: {os.path.basename(image_path)}")
        return encodings[0].tolist()

    except Exception as e:
        print(f"Image Encoding Error ({image_path}): {e}")
        return None


@router.post("/saveStudentFaceEncodings/{stu_regno}")
async def save_student_face_encodings(
    stu_regno: str,
    frontImg1: UploadFile = File(None),
    frontImg2: UploadFile = File(None),
    leftImg: UploadFile = File(None),
    rightImg: UploadFile = File(None),
):
    # Ensure directories exist
    os.makedirs("app/assets/Students", exist_ok=True)
    os.makedirs("app/assets", exist_ok=True)

    image_dict = {
        "frontImg1": frontImg1,
        "frontImg2": frontImg2,
        "leftImg": leftImg,
        "rightImg": rightImg
    }

    encodings_output = {}

    for img_key, img_file in image_dict.items():
        if img_file is None:
            encodings_output[img_key] = None
            continue

        try:
            # Save image to disk
            image_path = f"app/assets/Students/{stu_regno}_{img_key}.jpg"
            file_bytes = await img_file.read()

            if not file_bytes:
                encodings_output[img_key] = None
                continue

            with open(image_path, "wb") as f:
                f.write(file_bytes)

            # Generate encoding from saved image
            encoding = process_image_get_encoding_from_path(image_path)
            encodings_output[img_key] = encoding

        except Exception as e:
            print(f"Processing error ({img_key}): {e}")
            encodings_output[img_key] = None

    # JSON file path
    json_file_path = "app/assets/student_encodings.json"

    # Load existing JSON
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, "r") as f:
                data = json.load(f)
        except:
            data = {}
    else:
        data = {}

    # Update student entry
    data[stu_regno] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "encodings": encodings_output
    }

    # Save JSON
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "status": "success",
        "reg_no": stu_regno,
        "encodings_found": sum(1 for v in encodings_output.values() if v is not None),
        "message": "Student face encodings saved successfully"
    }
