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
    ```models/sam_vit_l_0b3195.encoder.onnx
    models/sam_vit_l_0b3195.decoder.onnx
    ```
3. Install Segment Anything ONNX using pip:
    ```bash
    pip install segment-anything-onnx
    ```
4. Predict a mask:
    ```python
    from segment_anything_onnx import predict_masks

    image = cv2.imread('args.image')
    prompt = json.load(open(args.prompt))

    predict_masks( 
        'models/sam_vit_l_0b3195.encoder.onnx',
        'models/sam_vit_l_0b3195.decoder.onnx',
        image,
        prompt,
        options )
    ```