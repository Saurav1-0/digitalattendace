
import cv2

from pathlib import Path
from collections import defaultdict

from .matcher import load_gallery, match_student


BASE_DIR = Path(__file__).resolve().parent.parent

DETECTOR_MODEL = BASE_DIR / "models/face_detection_yunet_2026may.onnx"
RECOGNIZER_MODEL = BASE_DIR / "models/face_recognition_sface_2021dec.onnx"
GALLERY_FILE = BASE_DIR / "data/student_gallery.npz"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def initialize_models():
    """Load the detector, recognizer and student gallery once."""

    recognizer = cv2.FaceRecognizerSF.create(
        str(RECOGNIZER_MODEL), ""
    )

    gallery_embeddings, gallery_ids = load_gallery(
        str(GALLERY_FILE)
    )

    return recognizer, gallery_embeddings, gallery_ids


def process_image(
    image_path,
    detector,
    recognizer,
    gallery_embeddings,
    gallery_ids,
    output_dir
):
    """Detect and recognize faces in one classroom photograph."""

    image = cv2.imread(str(image_path))

    if image is None:
        print(f"Could not read image: {image_path.name}")
        return None

    height, width = image.shape[:2]

    # Update detector input size for this photograph
    detector.setInputSize((width, height))

    output = image.copy()

    _, faces = detector.detect(image)

    photo_result = {
        "photo": image_path.name,
        "faces_detected": 0,
        "matched": [],
        "review": [],
        "unknown": 0,
        "detections": []
    }

    if faces is None:
        print(f"No faces detected in {image_path.name}")
    else:
        photo_result["faces_detected"] = len(faces)

        for face in faces:

            x, y, w, h = face[:4].astype(int)

            # Align face
            aligned_face = recognizer.alignCrop(
                image, face
            )

            # Extract embedding
            embedding = recognizer.feature(
                aligned_face
            ).flatten()

            # Match against saved student gallery
            result = match_student(
                embedding,
                gallery_embeddings,
                gallery_ids,
                recognizer
            )

            status = result["status"]
            candidate_id = result.get("candidate_id")
            student_id = result.get("student_id")
            score = result.get("best_score")

            # Prepare annotation and evidence
            if status == "matched":
                label = f"{student_id} ({score:.2f})"
                color = (0, 255, 0)
                photo_result["matched"].append(student_id)

            elif status == "review":
                label = f"Review: {candidate_id}"
                color = (0, 165, 255)
                photo_result["review"].append(candidate_id)

            else:
                label = "Unknown"
                color = (0, 0, 255)
                photo_result["unknown"] += 1

            cv2.rectangle(
                output,
                (x, y),
                (x + w, y + h),
                color,
                2
            )

            cv2.putText(
                output,
                label,
                (x, max(20, y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )

            photo_result["detections"].append({
                "status": status,
                "student_id": student_id,
                "candidate_id": candidate_id,
                "score": score
            })

    # Save annotated photograph
    output_path = output_dir / f"{image_path.stem}_result.jpg"

    cv2.imwrite(str(output_path), output)

    print(
        f"{image_path.name}: "
        f"{photo_result['faces_detected']} faces detected"
    )

    return photo_result


# def combine_results(photo_results):


def combine_results(photo_results):

    from collections import defaultdict

    student_evidence = defaultdict(int)

    total_faces = 0
    total_unknown = 0

    for photo in photo_results:

        total_faces += photo["faces_detected"]
        total_unknown += photo["unknown"]

        for detection in photo["detections"]:

            # Only faces passing the matching threshold
            if detection["status"] == "matched":

                student_id = detection["student_id"]

                if student_id is not None:
                    student_evidence[student_id] += 1

    detected_students = []

    for student_id, evidence_count in student_evidence.items():

        detected_students.append({
            "student_id": student_id,
            "evidence_count": evidence_count
        })

    return {
        "total_photos": len(photo_results),
        "total_faces_detected": total_faces,
        "unknown_faces": total_unknown,
        "detected_students": detected_students
    }

    """Combine evidence across all photographs in a session."""

    student_evidence = defaultdict(list)

    total_faces = 0
    total_unknown = 0

    for photo in photo_results:

        total_faces += photo["faces_detected"]
        total_unknown += photo["unknown"]

        for detection in photo["detections"]:

            candidate_id = detection["candidate_id"]

            if candidate_id is None:
                continue

            student_evidence[candidate_id].append({
                "photo": photo["photo"],
                "status": detection["status"],
                "score": detection["score"]
            })
    # print("student_evidence",student_evidence)

    detected_students = []
    review_students = []

    for student_id, evidence in student_evidence.items():

        statuses = {item["status"] for item in evidence}

        record = {
            "student_id": student_id,
            "photos_seen": len(evidence),
            "evidence": evidence
        }

        # A matched result in at least one photo is provisional evidence.
        if "matched" in statuses:
            record["status"] = "detected"
            detected_students.append(record)

        elif "review" in statuses:
            record["status"] = "review"
            review_students.append(record)

    return {
        "total_photos": len(photo_results),
        "total_faces_detected": total_faces,
        "unknown_faces": total_unknown,
        "detected_students": detected_students,
        "review_students": review_students
    }


def process_session(session_dir):

    session_dir = Path(session_dir)

    if not session_dir.is_dir():
        raise ValueError(f"Session folder not found: {session_dir}")

    image_paths = sorted(
        path for path in session_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not image_paths:
        raise ValueError("No classroom photographs found.")

    # Initialize models only once for the entire session
    recognizer, gallery_embeddings, gallery_ids = initialize_models()

    first_image = cv2.imread(str(image_paths[0]))

    if first_image is None:
        raise ValueError(f"Could not read {image_paths[0]}")

    height, width = first_image.shape[:2]

    detector = cv2.FaceDetectorYN.create(
        str(DETECTOR_MODEL),
        "",
        (width, height),
        0.8,
        0.3,
        5000
    )

    output_dir = session_dir / "results"
    output_dir.mkdir(exist_ok=True)

    photo_results = []

    for image_path in image_paths:

        result = process_image(
            image_path,
            detector,
            recognizer,
            gallery_embeddings,
            gallery_ids,
            output_dir
        )

        if result is not None:
            photo_results.append(result)

    session_result = combine_results(photo_results)

    return {
        "photos": photo_results,
        "summary": session_result
    }
