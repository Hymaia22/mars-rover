#!/usr/bin/env python3
"""Détecteur d'écarts sur les mesures de la suite de tests.

Lit un fichier de mesures au format de ops/metrics.csv, compare le dernier
lancement à la fenêtre de référence déclarée par bands.yaml et rend le
palier le plus élevé atteint (mean_stddev).
"""
from __future__ import annotations

import csv
import re
import statistics
import sys
from pathlib import Path

BANDS_PATH = Path(__file__).parent / "bands.yaml"


def read_bands(bands_path):
    """Lit fenêtre et paliers depuis bands.yaml, sans dépendance YAML."""
    text = Path(bands_path).read_text(encoding="utf-8")

    baseline_match = re.search(r"baseline:\s*rolling_(\d+)_runs", text)
    if not baseline_match:
        raise ValueError(f"baseline introuvable dans {bands_path}")
    window = int(baseline_match.group(1))

    tiers = []
    for match in re.finditer(r"(\d+)sigma:\s*\{(.*?)\}", text, re.DOTALL):
        threshold = int(match.group(1))
        action_match = re.search(r"action:\s*([A-Za-z_]+)", match.group(2))
        if action_match:
            tiers.append((threshold, action_match.group(1)))
    tiers.sort(key=lambda tier: tier[0])

    return window, tiers


def _rate(row):
    """Taux d'échec d'une ligne, ou None si illisible ou sans test exécuté."""
    try:
        echecs = int(row["echecs"])
        total = int(row["total"])
    except (TypeError, ValueError, KeyError):
        return None
    if total <= 0:
        return None
    return echecs / total


def read_rows(metrics_path):
    with open(metrics_path, newline="", encoding="utf-8") as f:
        lines = [line for line in f if not line.lstrip().startswith("#")]
    return list(csv.DictReader(lines))


def detect(metrics_path, bands_path=BANDS_PATH):
    """Calcule l'écart du dernier lancement par rapport à sa référence.

    Rend un dict {tier, action, today, reference, deviation}. tier vaut 0
    (aucune alerte) si le dernier lancement ou la référence sont illisibles
    ou insuffisants.
    """
    window, tiers = read_bands(bands_path)
    rows = read_rows(metrics_path)

    empty = {"tier": 0, "action": None, "today": None, "reference": None, "deviation": None}

    if not rows:
        return empty

    today_rate = _rate(rows[-1])
    if today_rate is None:
        return empty

    reference_rows = rows[-1 - window : -1]
    reference_rates = [r for r in (_rate(row) for row in reference_rows) if r is not None]

    if len(reference_rates) < 2:
        return {**empty, "today": today_rate}

    reference_mean = statistics.mean(reference_rates)
    reference_stdev = statistics.stdev(reference_rates)

    if reference_stdev == 0:
        deviation = 0.0 if today_rate == reference_mean else float("inf")
    else:
        deviation = abs(today_rate - reference_mean) / reference_stdev

    tier = 0
    action = None
    for threshold, tier_action in tiers:
        if deviation >= threshold:
            tier = threshold
            action = tier_action

    return {
        "tier": tier,
        "action": action,
        "today": today_rate,
        "reference": reference_mean,
        "deviation": deviation,
    }


def main(argv):
    if len(argv) != 2:
        print("usage : detect.py <mesures.csv>", file=sys.stderr)
        return 2

    result = detect(Path(argv[1]), BANDS_PATH)

    today = result["today"]
    reference = result["reference"]
    deviation = result["deviation"]

    print(f"mesure du jour : {today if today is not None else 'indisponible'}")
    print(f"moyenne de référence : {reference if reference is not None else 'indisponible'}")
    print(f"écart : {deviation if deviation is not None else 'indisponible'}")
    print(f"palier atteint : {result['tier']}")
    print(f"action : {result['action'] if result['action'] is not None else '(aucune)'}")

    return result["tier"]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
