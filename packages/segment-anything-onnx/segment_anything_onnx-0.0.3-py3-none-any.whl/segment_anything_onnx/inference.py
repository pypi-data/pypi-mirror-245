# Derived from https://github.com/vietanhdev/samexporter

import sys
import pathlib
import cv2
import numpy as np

sys.path.append(".")
from .sam_onnx import SegmentAnythingONNX


def predict_masks( encoder_model_path, decoder_model_path, image, prompt, options ):

    model = SegmentAnythingONNX(
        encoder_model_path,
        decoder_model_path,
    )

    embedding = model.encode(image)
    masks = model.predict_masks(embedding, prompt)

    # Save the masks as a single image.
    mask = np.zeros((masks.shape[2], masks.shape[3], 3), dtype=np.uint8)
    for m in masks[0, :, :, :]:
        mask[m > 0.0] = [255, 0, 0]

    # Binding image and mask
    visualized = cv2.addWeighted(image, 0.5, mask, 0.5, 0)

    # Draw the prompt points and rectangles.
    for p in prompt:
        if p["type"] == "point":
            color = (
                (0, 255, 0) if p["label"] == 1 else (0, 0, 255)
            )  # green for positive, red for negative
            cv2.circle(visualized, (p["data"][0], p["data"][1]), 10, color, -1)
        elif p["type"] == "rectangle":
            cv2.rectangle(
                visualized,
                (p["data"][0], p["data"][1]),
                (p["data"][2], p["data"][3]),
                (0, 255, 0),
                2,
            )

    output = options['output']
    if output is not None:
        pathlib.Path(output).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output, visualized)

    if options['show']:
        cv2.imshow("Result", visualized)
        cv2.waitKey(0)
