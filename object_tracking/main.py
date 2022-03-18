import cv2
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

tracker = cv2.TrackerKCF_create()
success, img = cap.read()
bbox = cv2.selectROI("tracking", img, False)
tracker.init(img, bbox)

while True:

    success, img = cap.read()

    success, bbox = tracker.update(img)

    if success:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2, 1)
        cv2.putText(img, "Object tracking", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    else:
        cv2.putText(img, "Object lost", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Input", img)

    # press q to exit
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
