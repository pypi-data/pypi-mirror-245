import argparse
from pathlib import Path

import torch
import torchaudio
from tqdm import tqdm

from .inference import denoise, enhance


@torch.inference_mode()
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("in_dir", type=Path, help="Path to input audio folder")
    parser.add_argument("out_dir", type=Path, help="Output folder")
    parser.add_argument(
        "--run_dir",
        type=Path,
        default=None,
        help="Path to the enhancer run folder, if None, use the default model",
    )
    parser.add_argument(
        "--suffix",
        type=str,
        default=".wav",
        help="Audio file suffix",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="Device to use for computation, recommended to use CUDA",
    )
    parser.add_argument(
        "--denoise_only",
        action="store_true",
        help="Only apply denoising without enhancement",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.5,
        help="Denoise strength for enhancement (0.0 to 1.0)",
    )
    parser.add_argument(
        "--solver",
        type=str,
        default="midpoint",
        choices=["midpoint", "rk4", "euler"],
        help="Numerical solver to use",
    )
    parser.add_argument(
        "--nfe",
        type=int,
        default=64,
        help="Number of function evaluations",
    )

    args = parser.parse_args()

    run_dir = args.run_dir

    paths = list(args.in_dir.glob(f"**/*{args.suffix}"))

    if len(paths) == 0:
        print(f"No {args.suffix} files found in the following path: {args.in_dir}")
        return

    pbar = tqdm(paths)

    for path in pbar:
        pbar.set_description(f"Processing {path}")
        dwav, sr = torchaudio.load(path)
        dwav = dwav.mean(0)
        if args.denoise_only:
            hwav, sr = denoise(
                dwav=dwav,
                sr=sr,
                device=args.device,
                run_dir=args.run_dir,
            )
        else:
            hwav, sr = enhance(
                dwav=dwav,
                sr=sr,
                device=args.device,
                nfe=args.nfe,
                solver=args.solver,
                alpha=args.alpha,
                run_dir=run_dir,
            )
        out_path = args.out_dir / path.relative_to(args.in_dir)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        torchaudio.save(out_path, hwav[None], sr)


if __name__ == "__main__":
    main()
