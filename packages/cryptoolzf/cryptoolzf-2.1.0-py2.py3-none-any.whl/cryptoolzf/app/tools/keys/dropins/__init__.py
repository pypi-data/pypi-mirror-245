from pathlib import Path
from cryptoolzf.utils import ROOT_DIR
from importlib import import_module

dropins_po = Path(ROOT_DIR + "/app/tools/keys/dropins")

__all__ = []

for dropin_po in dropins_po.iterdir():
    if dropin_po.name != "__init__.py" and dropin_po.name != "__pycache__":
        import_module(
            "cryptoolzf.app.tools.keys.dropins." + dropin_po.with_suffix("").stem
        )
        __all__.append(dropin_po.with_suffix("").stem)
