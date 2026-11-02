import cv2
from .recognizer import recognize_faces

def detect_faces(image_path: str, model_path: str):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    height, width = image.shape[:2]

    detector = cv2.FaceDetectorYN.create(
        model_path,
        "",
        (width, height),
        0.8,   # Initial detection threshold, to detect regions that contains face or not, its show detection confidence
        0.3,   # NMS threshold
        50000   # Maximum detections
    )

    _, faces = detector.detect(image)

    return image, faces


if __name__ == "__main__":

# face detection
    image, faces = detect_faces(
        "data/classroom_images/friends_group4.jpg",
        "models/face_detection_yunet_2026may.onnx"
    )

    if faces is not None:
        for face in faces:
            print("Face detected:", face)
            x, y, w, h = face[:4].astype(int)

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

    print("Faces detected:", 0 if faces is None else len(faces))

    cv2.imshow("FaceMatch - Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# embedding generation
    results = recognize_faces(
    image,
    faces,
    "models/face_recognition_sface_2021dec.onnx"
)

print("Faces processed:", len(results))

if results:
    print(
        "Embedding shape:",
        results[0]["embedding"].shape
    )
# print(results[0]["aligned_face"])
# print(results[0]["embedding"])