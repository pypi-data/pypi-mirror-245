import os
import json

from typing import List, Dict, Union, Optional, Any

from pathlib import Path

from re import finditer


def process_pem_file(
    pem_encoded: List[str], context_chunks: List[Union[str, List[str]]]
) -> List[str]:
    results = []

    for pem_text in pem_encoded:
        matches = [match for match in finditer(r"-+(BEGIN|END) [ A-Z]+-+", pem_text)]

        if len(matches) % 2 != 0:
            raise RuntimeError(
                f"{context_chunks[0]} :: FileDummy._lambda: File {context_chunks[1][pem_encoded.index(pem_text)]} has an odd number of begin and end lines!"
            )

        for i in range(0, len(matches), 2):
            results.append(pem_text[matches[i].start() : matches[i + 1].end()])

    return results


def process_naked_b64(
    b64_lines_block: List[str], context_chunks: List[Union[str, List[str]]]
) -> List[str]:
    results = []

    for block in b64_lines_block:
        lines = block.split("=")
        for i in range(len(lines) - 1):
            results.append(lines[i].strip() + "=")

    return results


def match_value(cases: Dict[str, Any], value: Any) -> Any:
    if value in cases:
        cases = cases[value]
    else:
        raise ValueError("utils.match_value :: matched is None!")
    return cases


def match_values(cases: Dict[str, Any], *values: List[Any]) -> Any:
    for value in values:
        if value in cases:
            cases = cases[value]
        else:
            raise ValueError("utils.match_values :: matched is None!")
    return cases


def get_next_free_po(po: Path) -> Path:
    counter = 1
    stem = po.stem
    while po.exists():
        po = po.with_stem(f"{stem}{counter}")
        counter += 1
    return po


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # cryptoolzf root


def get_resource(filename: str) -> Any:
    with (Path(ROOT_DIR) / "resources" / filename).open(mode="r") as fo:
        return json.load(fo)
    raise RuntimeError("utils.get_resource: should have never reached this point!")
