# SA

> A backend service which implement [segment anything](https://github.com/facebookresearch/segment-anything)

## Requirement environment

- `Python`: `^3.11`
- `poetry`: `^1.x`
- [`Segment Anything Model`](https://github.com/facebookresearch/segment-anything?tab=readme-ov-file#model-checkpoints)

> `poetry` installation guide: [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

## Installation dependencies

```bash
poetry install
```

## Configuration file

- `.env`

```properties
# COS config
COS_SECRET_ID=<your cos secret id>
COS_SECRET_KEY=<your cos secret key>
COS_REGION=<your cos region>
COS_BUCKET=<your cos bucket>

# SAM
SAM_MODEL_CHECKPOINT=./sam_vit_h_4b8939.pth
SAM_MODEL_TYPE=vit_h
```

## Start server

- run with `python`

```bash
python main.py
```

- run with `uvicorn`

```bash
uvicorn main:app --reload
```

- run with `poetry`

```bash
poetry run uvicorn main:app --reload
```
