import argparse
from pathlib import Path

import torch
import torchaudio

from .inference import denoise, enhance


@torch.inference_mode()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("in_dir", type=Path, help="Path to input audio folder")
    parser.add_argument("out_dir", type=Path, default="syn_out", help="Output folder")
    parser.add_argument("--run_dir", type=Path, default="runs/enhancer_stage2", help="Path to run folder")
    parser.add_argument("--suffix", type=str, default=".wav", help="File suffix")
    parser.add_argument("--device", type=str, default="cuda", help="Device")
    parser.add_argument("--denoise_only", action="store_true", help="Only denoise")
    args = parser.parse_args()

    for path in args.in_dir.glob(f"**/*{args.suffix}"):
        print(f"Processing {path} ..")
        dwav, sr = torchaudio.load(path)
        if args.denoise_only:
            hwav, sr = denoise(dwav[0], sr, args.run_dir, args.device)
        else:
            hwav, sr = enhance(dwav[0], sr, args.run_dir, args.device)
        out_path = args.out_dir / path.relative_to(args.in_dir)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        torchaudio.save(out_path, hwav[None], sr)


if __name__ == "__main__":
    main()
