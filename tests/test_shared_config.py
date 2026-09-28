from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "parameter_fitter"))

import fit_shared


def test_graphene_shared_example_schema():
    path = ROOT / "paper_benchmark" / "examples" / "graphene_vacancies_shared.yaml"
    _, shared, systems = fit_shared.load_config(path)
    fit_shared.validate_schema(shared, systems)
    assert len(systems) == 4
    assert [s["role"] for s in systems[:3]] == ["train", "train", "train"]
    assert systems[3]["role"] == "test"
    assert shared["fit_window"] == [-2.0, 2.0]
