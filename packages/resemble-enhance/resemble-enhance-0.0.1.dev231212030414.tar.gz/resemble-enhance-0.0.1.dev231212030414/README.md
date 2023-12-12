---
title: Resemble Enhance
emoji: 🚀
colorFrom: red
colorTo: pink
sdk: gradio
sdk_version: 4.8.0
app_file: app.py
pinned: false
license: mit
---

# Resemble Enhance

Resemble Enhance is an AI-powered tool that aims to improve the overall quality of speech by performing denoising and enhancement. It consists of two modules: a denoiser, which separates speech from a noisy audio, and an enhancer, which further boosts the perceptual audio quality by restoring audio distortions and extending the audio bandwidth. The two models are trained on high-quality 44.1kHz speech data that guarantees the enhancement of your speech with high quality.

## Usage

### Installation

```bash
pip install resemble-enhance
```

### Enhance

```
resemble_enhance in_dir out_dir
```

### Denoise only

```
resemble_enhance in_dir out_dir --denoise_only
```

### Gradio

To serve the gradio demo, run:

```
python app.py
```

## Train your own model

### Data Preparation

You need to prepare a foreground speech dataset and a background non-speech dataset. In addition, you need to prepare a RIR dataset.

```bash
data
├── fg
│   ├── 00001.wav
│   └── ...
├── bg
│   ├── 00001.wav
│   └── ...
└── rir
    ├── 00001.wav
    └── ...
```

### Training

#### Denoiser Warmup

Though the denoiser is trained jointly with the enhancer, it is recommended for a warmup training first.

```bash
python -m resemble_enhance.denoiser.train --yaml config/denoiser.yaml
```

#### Enhancer

##### Stage 1

```bash
python -m resemble_enhance.enhancer.train --yaml config/enhancer_stage1.yaml
```

##### Stage 2

```bash
python -m resemble_enhance.enhancer.train --yaml config/enhancer_stage2.yaml
```
