# segment-anything-onnx

Use ONNX models for Segment Anything inference.

Special thanks to:
- [Viet-Anh NGUYEN](https://github.com/vietanhdev) for creating the [SAM Exporter](https://github.com/vietanhdev/samexporter) libraries from which these files are derived.
- The [Segment Anything](https://github.com/facebookresearch/segment-anything) team at Meta AI Research


## Usage from Source

1. Clone Segment Anything ONNX from Github
    ```bash
    git clone git@github.com:whatstyle-ai/segment-anything-onnx.git
    cd segment-anything-onnx
    pip install -e .
    ```
2. Use the [SAM Exporter](https://github.com/vietanhdev/samexporter) to generate the ONNX models
3. Copy the ONNX models to the segment-anything-onnx/models directory
4. Predict some masks 
    ```bash
    cd segment-anything-onnx
    ./demo.sh
    ```

## Usage from pip install

1. Use the [SAM Exporter](https://github.com/vietanhdev/samexporter) to generate the ONNX models, or obtain the ONNX models from another source
2. Copy the ONNX models to a "models" directory, such as:
    ```
    models/sam_vit_l_0b3195.encoder.onnx
    models/sam_vit_l_0b3195.decoder.onnx
    ```
3. Install Segment Anything ONNX using pip:
    ```bash
    pip install segment-anything-onnx
    ```
4. Predict a mask:
    ```python
import cv2
import urllib.request
import numpy as np

from segment_anything_onnx.inference import predict_masks


def load_image(uri):
    if( uri.startswith('https://') or uri.startswith('http://') ):
        req = urllib.request.urlopen(uri)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        return img
    else: 
        return cv2.imread(uri)  # uri is just a local file path


encoder_model_path = './models/sam_vit_l_0b3195.encoder.onnx'
decoder_model_path = './models/sam_vit_l_0b3195.decoder.onnx'
image = load_image( 'https://raw.githubusercontent.com/whatstyle-ai/segment-anything-onnx/main/examples/laura.jpg' )
prompt = [
    { 'type': 'point', 'data': [1750, 300], 'label': 0 },
    { 'type': 'rectangle', 'data': [611, 655, 2712, 4500] }
]
options = {
    'show': True,
    'output': './output/laura-L.png'
}

predict_masks( encoder_model_path, decoder_model_path, image, prompt, options )
    ```