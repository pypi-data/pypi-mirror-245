# Derived from https://github.com/vietanhdev/samexporter

import argparse
import cv2
import json

# sys.path.append(".")

from .inference import predict_masks

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "--encoder_model",
    type=str,
    default="models/sam_vit_l_0b3195.encoder.onnx",
    help="Path to the ONNX encoder model",
)
argparser.add_argument(
    "--decoder_model",
    type=str,
    default="models/sam_vit_l_0b3195.decoder.onnx",
    help="Path to the ONNX decoder model",
)
argparser.add_argument(
    "--image",
    type=str,
    default="examples/laura.jpg",
    help="Path to the image",
)
argparser.add_argument(
    "--prompt",
    type=str,
    default="examples/laura_prompt.json",
    help="Path to the image",
)
argparser.add_argument(
    "--output",
    type=str,
    default=None,
    help="Path to the output image",
)
argparser.add_argument(
    "--show",
    action="store_true",
    help="Show the result",
)
args = argparser.parse_args()

image = cv2.imread(args.image)
prompt = json.load(open(args.prompt))
options = {
	'show': args.show,
	'output': args.output
}

predict_masks( args.encoder_model, args.decoder_model, image, prompt, options )