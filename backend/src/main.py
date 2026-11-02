
# import cv2
# import numpy as np

# from pathlib import Path

# from .matcher import load_gallery, match_student


# BASE_DIR = Path(__file__).resolve().parent.parent

# DETECTOR_MODEL = BASE_DIR / "models/face_detection_yunet_2026may.onnx"
# RECOGNIZER_MODEL = BASE_DIR / "models/face_recognition_sface_2021dec.onnx"

# GALLERY_FILE = BASE_DIR / "data/student_gallery.npz"

# group_photo = "friends_group4.jpg"
# classroom_photo = "classroom4.jpg"

# IMAGE_PATH = BASE_DIR / "data/classroom_images" /classroom_photo
# # friends_group1


# def main():

#     # Load classroom image
#     image = cv2.imread(str(IMAGE_PATH))
    

#     if image is None:
#         raise ValueError("Classroom image not found.")
#     output = image.copy()

#     height, width = image.shape[:2]

#     # Initialize YuNet
#     detector = cv2.FaceDetectorYN.create(
#         str(DETECTOR_MODEL),
#         "",
#         (width, height),
#         0.8,
#         0.3,
#         5000
#     )

#     # Initialize SFace
#     recognizer = cv2.FaceRecognizerSF.create(
#         str(RECOGNIZER_MODEL),
#         ""
#     )

#     # Load student gallery
#     gallery_embeddings, gallery_ids = load_gallery(
#         str(GALLERY_FILE)
#     )

#     # Detect faces
#     _, faces = detector.detect(image)

#     if faces is None:
#         print("No faces detected.")
#         return

#     print("Faces detected:", len(faces))

#     for face in faces:

#         x, y, w, h = face[:4].astype(int)

#         # Align face
#         aligned_face = recognizer.alignCrop(
#             image,
#             face
#         )

#         # Extract embedding
#         embedding = recognizer.feature(
#             aligned_face
#         ).flatten()

#         # Find student
#         result = match_student(
#             embedding,
#             gallery_embeddings,
#             gallery_ids,
#             recognizer
#         )

#         status = result["status"]
#         student_id = result["student_id"]

#         if status == "matched":
#             label = f"{student_id} ({result['best_score']:.2f})"
#             color = (0, 255, 0)

#         elif status == "review":
#             label = f"Review: {result['candidate_id']}"
#             color = (0, 165, 255)

#         else:
#             label = "Unknown"
#             label = f"False Match: {result['candidate_id']} ({result['best_score']:.2f})"
#             color = (0, 0, 255)

#         # Draw bounding box
#         cv2.rectangle(
#             output,
#             (x, y),
#             (x + w, y + h),
#             color,
#             2
#         )

#         # Draw label
#         cv2.putText(
#             output,
#             label,
#             (x, max(20, y - 10)),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.5,
#             color,
#             2
#         )

#         print(
#             status,
#             result.get("candidate_id"),
#             result.get("best_score")
#         )


#     # Display and save
#     print("Original dimensions:", image.shape)
#     print("Output dimensions:", output.shape)

#     cv2.imwrite(
#         "data/classroom_images/result.jpg",
#         output
#     )

#     cv2.namedWindow(
#         "FaceMatch - Recognition",
#         cv2.WINDOW_NORMAL
#     )
#     cv2.imshow("FaceMatch - Recognition", output)
 

#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()



#     preview = cv2.resize(
#                     output,
#                     (1200, 800)
#                     )
#     cv2.imshow("FaceMatch", preview)

#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()




































from pathlib import Path

from .session import process_session


BASE_DIR = Path(__file__).resolve().parent.parent

SESSION_DIR = BASE_DIR / "data/classroom_images/session_001"


def main():

    result = process_session(SESSION_DIR)

    summary = result["summary"]

    print("\n========== SESSION REPORT ==========")

    print("Total photographs:", summary["total_photos"])
    print("Total faces detected:", summary["total_faces_detected"])
    print("Unknown faces:", summary["unknown_faces"])

    print("\n--- Detected Students (Provisional) ---")

    for student in summary["detected_students"]:
        print(
            student["student_id"],
            "| Evidence count:",
            student["evidence_count"]
        )


    print("\nAnnotated photographs saved in:")
    print(SESSION_DIR / "results")


if __name__ == "__main__":
    main()
