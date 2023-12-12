import logging
from functools import cache

import torch

from ..inference import inference
from .train import Enhancer, HParams

logger = logging.getLogger(__name__)


@cache
def load_enhancer(run_dir, device):
    hp = HParams.load(run_dir)
    enhancer = Enhancer(hp)
    path = run_dir / "ds" / "G" / "default" / "mp_rank_00_model_states.pt"
    state_dict = torch.load(path, map_location="cpu")["module"]
    enhancer.load_state_dict(state_dict)
    enhancer.eval()
    enhancer.to(device)
    return enhancer


@torch.inference_mode()
def denoise(dwav, sr, run_dir, device):
    enhancer = load_enhancer(run_dir, device)
    return inference(model=enhancer.denoiser, dwav=dwav, sr=sr, device=device)


@torch.inference_mode()
def enhance(dwav, sr, run_dir, device, nfe=32, solver="midpoint", alpha=0.5):
    assert 0 < nfe <= 128, f"nfe must be in (0, 128], got {nfe}"
    assert solver in ("midpoint", "rk4", "euler"), f"solver must be in ('midpoint', 'rk4', 'euler'), got {solver}"
    assert 0 <= alpha <= 1, f"alpha must be in [0, 1], got {alpha}"
    enhancer = load_enhancer(run_dir, device)
    enhancer.configurate_(nfe=nfe, solver=solver, alpha=alpha)
    return inference(model=enhancer, dwav=dwav, sr=sr, device=device)
