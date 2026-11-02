
import cv2
import numpy as np

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DETECTOR_MODEL = BASE_DIR / "models/face_detection_yunet_2026may.onnx"
RECOGNIZER_MODEL = BASE_DIR / "models/face_recognition_sface_2021dec.onnx"

ENROLLMENT_DIR = BASE_DIR / "data/enrollment"
OUTPUT_FILE = BASE_DIR / "data/student_gallery.npz"


def create_embedding(image_path, detector, recognizer):

    image = cv2.imread(str(image_path))

    if image is None:
        print(f"Cannot read: {image_path}")
        return None

    height, width = image.shape[:2]

    detector.setInputSize((width, height))

    _, faces = detector.detect(image)

    if faces is None or len(faces) == 0:
        print(f"No face detected: {image_path}")
        return None

    if len(faces) != 1:
        print(f"Expected one face: {image_path}")
        return None

    # Align and crop the face
    aligned_face = recognizer.alignCrop(image, faces[0])

    # Generate SFace embedding
    embedding = recognizer.feature(aligned_face)

    return embedding.flatten()


def build_student_gallery():

    detector = cv2.FaceDetectorYN.create(
        str(DETECTOR_MODEL),
        "",
        (320, 320),
        0.8,
        0.3,
        5000
    )

    recognizer = cv2.FaceRecognizerSF.create(
        str(RECOGNIZER_MODEL),
        ""
    )

    all_embeddings = []
    all_student_ids = []

    for student_folder in ENROLLMENT_DIR.iterdir():

        if not student_folder.is_dir():
            continue

        student_id = student_folder.name

        print(f"\nProcessing student: {student_id}")

        for image_path in student_folder.iterdir():

            if image_path.suffix.lower() not in {
                ".jpg", ".jpeg", ".png"
            }:
                continue

            embedding = create_embedding(
                image_path,
                detector,
                recognizer
            )

            if embedding is not None:
                all_embeddings.append(embedding)
                all_student_ids.append(student_id)

                print(f"  Registered: {image_path.name}")

    if not all_embeddings:
        raise ValueError("No valid student embeddings generated.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        OUTPUT_FILE,
        embeddings=np.array(all_embeddings),
        student_ids=np.array(all_student_ids)
    )

    print("\nGallery created successfully!")
    print("Total reference images:", len(all_embeddings))
    print("Total students:", len(set(all_student_ids)))
    print("Saved at:", OUTPUT_FILE)


if __name__ == "__main__":
    build_student_gallery()
