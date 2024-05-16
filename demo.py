import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np
from src import util
from src.body import Body
import math

body_estimation = Body("model/body_pose_model.pth")

test_image = "images/Screenshot 2024-04-17 181917.png"
oriImg = cv2.imread(test_image)
candidate, subset = body_estimation(oriImg)

canvas = copy.deepcopy(oriImg)
canvas = util.draw_bodypose(canvas, candidate, subset)

plt.imshow(canvas[:, :, [2, 1, 0]])
plt.axis("off")
plt.show()


def person_list(candidate, subset):
    people = []
    for s in subset:
        new_person = []
        for idx, p in enumerate(s[:-2]):  # Include the index of the point in the array
            if p >= 0:  # Ensure the index is valid
                c = candidate[int(p)]
                new_person.append(
                    (c[0], c[1], idx)
                )  # Append the x, y coordinates along with the point index
            else:
                new_person.append(None)  # Append None for invalid keypoints
        people.append(new_person)
    return people


def draw_colored_bodypose(canvas, people):
    stickwidth = 4
    limbSeq = [
        [1, 2],
        [1, 5],
        [2, 3],
        [3, 4],
        [5, 6],
        [6, 7],
        [1, 8],
        [8, 9],
        [9, 10],
        [1, 11],
        [11, 12],
        [12, 13],
        [1, 0],
        [0, 14],
        [14, 16],
        [0, 15],
        [15, 17],
    ]

    num_people = len(people)
    colors = [plt.cm.hsv(i / float(num_people)) for i in range(num_people)]
    colors = [
        (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255)) for c in colors
    ]  # Convert from RGB to BGR for OpenCV

    for person_idx, person in enumerate(people):
        for _, keypoint in enumerate(person):
            if keypoint:
                x, y, _ = keypoint
                cv2.circle(
                    canvas, (int(x), int(y)), 4, colors[person_idx], thickness=-1
                )

        for _, (start_idx, end_idx) in enumerate(limbSeq):
            start_point = (
                person[start_idx]
                if start_idx < len(person) and person[start_idx]
                else None
            )
            end_point = (
                person[end_idx] if end_idx < len(person) and person[end_idx] else None
            )
            if start_point and end_point:
                x1, y1, _ = start_point
                x2, y2, _ = end_point
                mX = np.mean([x1, x2])
                mY = np.mean([y1, y2])
                length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
                polygon = cv2.ellipse2Poly(
                    (int(mX), int(mY)),
                    (int(length / 2), stickwidth),
                    int(angle),
                    0,
                    360,
                    1,
                )
                cv2.fillConvexPoly(canvas, polygon, colors[person_idx])

    return canvas


def find_lifter(people, image_shape):
    """
    Finds the person closest to the middle of the x-axis and the bottom of the y-axis in the image.

    Parameters:
    - people (list): A list of lists, where each inner list contains tuples (x, y) of detected keypoints for one person.
    - image_shape (tuple): A tuple indicating the shape of the image (height, width).

    Returns:
    - The list of keypoints for the person closest to the desired location.
    """
    # Define the target point as being at the horizontal center, and the very bottom of the image
    target_point = np.array([image_shape[1] / 2, image_shape[0] * (3 / 4)])

    min_distance = float("inf")
    closest_person = None

    for person in people:
        valid_points = [np.array([p[0], p[1]]) for p in person if p is not None]
        if valid_points:
            # Calculate the average location of keypoints to represent this person's position
            person_position = np.mean(valid_points, axis=0)
            # Calculate Euclidean distance from this person's position to the target point
            distance = np.linalg.norm(target_point - person_position)
            if distance < min_distance:
                min_distance = distance
                closest_person = person

    return closest_person


def draw_single_person(canvas, person, color=(255, 0, 0)):
    stickwidth = 4
    limbSeq = [
        [1, 2],
        [1, 5],
        [2, 3],
        [3, 4],
        [5, 6],
        [6, 7],
        [1, 8],
        [8, 9],
        [9, 10],
        [1, 11],
        [11, 12],
        [12, 13],
        [1, 0],
        [0, 14],
        [14, 16],
        [0, 15],
        [15, 17],
    ]

    for idx, keypoint in enumerate(person):
        if keypoint:
            x, y, _ = keypoint
            cv2.circle(canvas, (int(x), int(y)), 4, color, thickness=-1)

    for _, (start_idx, end_idx) in enumerate(limbSeq):
        start_point = (
            person[start_idx] if start_idx < len(person) and person[start_idx] else None
        )
        end_point = (
            person[end_idx] if end_idx < len(person) and person[end_idx] else None
        )
        if start_point and end_point:
            x1, y1, _ = start_point
            x2, y2, _ = end_point
            mX = np.mean([x1, x2])
            mY = np.mean([y1, y2])
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            polygon = cv2.ellipse2Poly(
                (int(mX), int(mY)), (int(length / 2), stickwidth), int(angle), 0, 360, 1
            )
            cv2.fillConvexPoly(canvas, polygon, color)

    return canvas


people = person_list(candidate, subset)
centermost_person = find_lifter(people, oriImg.shape)
canvas = copy.deepcopy(oriImg)
canvas = draw_single_person(canvas, centermost_person)
plt.imshow(canvas[:, :, [2, 1, 0]])
plt.axis("off")
plt.show()
