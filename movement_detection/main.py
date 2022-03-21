import cv2
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not capture.isOpened():
    raise IOError("Cannot open webcam")

background = None

while True:

    check, frame = capture.read()
    if not check:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    if background is None:
        background = gray
        continue

    diff = cv2.absdiff(background, gray)
    threshold_frame = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=10)

    contours, _ = cv2.findContours(
        threshold_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 100:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Input", frame)

    # press q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()
