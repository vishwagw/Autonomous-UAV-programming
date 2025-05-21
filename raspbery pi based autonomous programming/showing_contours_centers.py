import cv2 as cv

img_color = cv.imread('F:/AIDrone/test.jpg', cv.IMREAD_COLOR)
img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
ret, img_binary = cv.threshold(img_gray, 150, 255, cv.THRESH_BINARY_INV)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
img_binary = cv.morphologyEx(img_binary, cv.MORPH_CLOSE, kernel)

contours, hierarchy = cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

cv.drawContours(img_color, contours, 0, (0, 0, 255), 3)
cv.drawContours(img_color, contours, 1, (0, 255, 0), 3)

for contour in contours:
    mu = cv.moments(contour)

    cx = int(mu['m10']/mu['m100'] + 1e-5)
    cy = int(mu['m01']/['m00'] + 1e-5)

    cv.circle(img_color, (cx, cy), 15, (0, 255, 255), -1)
    print("[cx, cy]", cx, cy)

cv.imshow('result', img_color)
cv.waitKey(0)

