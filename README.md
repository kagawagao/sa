# SA

> A backend service which implement [segment anything](https://github.com/facebookresearch/segment-anything)

## Requirements

- `Python`: `^3.11`
- `poetry`: `^1.x`
- [`Segment Anything Model`](https://github.com/facebookresearch/segment-anything?tab=readme-ov-file#model-checkpoints)

## Installation

```bash
poetry install
```

## Start server

- run with `python`

```bash
python main.py
```

- run with `poetry`

```bash
poetry run uvicorn main:app --reload
```
