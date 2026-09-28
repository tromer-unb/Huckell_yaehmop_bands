from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "parameter_fitter"))
from image_target import load_band_image, trace_bands


def test_mos2_image_trace():
    image = ROOT / "parameter_fitter/examples/mos2/band.png"
    target = load_band_image(image, -15.0, 11.0)
    x, bands, counts, seed = trace_bands(target, 17, nx=401)
    assert bands.shape == (401, 17)
    assert np.isfinite(bands).all()
    gap = float(bands[:, 9].min() - bands[:, 8].max())
    assert 1.60 < gap < 1.70
    assert 0 <= seed < 401
