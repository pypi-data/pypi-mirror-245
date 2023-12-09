# segment-anything-onnx

Use ONNX models for Segment Anything inference.

Special thanks to [Viet-Anh NGUYEN](https://github.com/vietanhdev) for creating the [SAM Exporter](https://github.com/vietanhdev/samexporter) libraries from which these files are derived.

## Installation

From PyPi:

```bash
pip install segment-anything-onnx
```

From source:

```bash
git clone git@github.com:whatstyle-ai/segment-anything-onnx.git
cd segment-anything-onnx
pip install -e .
```

## Usage

1. Use the [SAM Exporter](https://github.com/vietanhdev/samexporter) to generate the ONNX models
2. Copy the ONNX models to the segment-anything-onnx/models directory
3. Run inference 
    ```bash
    python -m segment_anything_onnx.inference \
        --encoder_model ./models/sam_vit_l_0b3195.encoder.onnx \
        --decoder_model ./models/sam_vit_l_0b3195.decoder.onnx \
        --image ./examples/laura.jpg \
        --prompt ./examples/laura_prompt.json \
        --output ./output/laura-L.png \
        --show
    ```
