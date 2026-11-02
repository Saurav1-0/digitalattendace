
import cv2
import numpy as np


# OpenCV SFace reference threshold.
# Must be validated on your own dataset.
COSINE_THRESHOLD = 0.45

# Initial ambiguity margin for experimentation.
# Calibrate this using validation images.
MINIMUM_MARGIN = 0.05


def load_gallery(gallery_path):

    data = np.load(gallery_path)

    embeddings = data["embeddings"]
    student_ids = data["student_ids"]

    return embeddings, student_ids


def match_student(
    query_embedding,
    gallery_embeddings,
    gallery_student_ids,
    recognizer
):

    scores_by_student = {}

    for stored_embedding, student_id in zip(
        gallery_embeddings,
        gallery_student_ids
    ):

        score = recognizer.match(
            query_embedding.reshape(1, -1).astype(np.float32),
            stored_embedding.reshape(1, -1).astype(np.float32),
            cv2.FaceRecognizerSF_FR_COSINE
        )

        student_id = str(student_id)

        # Keep the highest score for each student
        scores_by_student[student_id] = max(
            scores_by_student.get(student_id, -1.0),
            float(score)
        )

    ranked = sorted(
        scores_by_student.items(),
        key=lambda item: item[1],
        reverse=True
    )

    if not ranked:
        return {
            "status": "unknown",
            "student_id": None,
            "best_score": None
        }

    best_student, best_score = ranked[0]

    second_score = ranked[1][1] if len(ranked) > 1 else -1.0

    margin = best_score - second_score

    if best_score < COSINE_THRESHOLD:
        status = "unknown"

    elif margin < MINIMUM_MARGIN:
        status = "review"

    else:
        status = "matched"

    return {
        "status": status,
        "student_id": best_student if status == "matched" else None,
        "candidate_id": best_student,
        "best_score": best_score,
        "second_score": second_score,
        "margin": margin,
        "all_scores": ranked
    }
