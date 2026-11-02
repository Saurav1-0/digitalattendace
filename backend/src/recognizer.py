
import cv2
import numpy as np


def recognize_faces(
    image,
    detected_faces,
    sface_model_path
):
    recognizer = cv2.FaceRecognizerSF.create(
        sface_model_path,
        ""
    )

    results = []

    if detected_faces is None:
        return results

    for face in detected_faces:
        # 1. Align and crop the detected face
        aligned_face = recognizer.alignCrop(
            image,
            face
        )

        # 2. Generate the face embedding
        embedding = recognizer.feature(
            aligned_face
        )

        # 3. Save the embedding for later matching
        results.append({
            "aligned_face": aligned_face,
            "embedding": embedding
        })

    return results
