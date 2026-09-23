from ops.detect import detect

BANDS = """metric: ci_test_failure_rate
baseline: rolling_5_runs
rules: mean_stddev
tiers:
  1sigma: { action: log }
  2sigma: { action: diagnose,
            tools: "Read,Grep,Bash(make test)" }
  3sigma: { action: propose,
            routes: [pull_request] }
"""
HEADER = "lancement,echecs,total,sujet\n"

# Référence à 5 lancements, quasi stable (4 lancements sans échec, 1 avec
# 20 échecs sur 1000), utilisée par plusieurs scénarios ci-dessous.
REFERENCE_ROWS = [(0, 1000), (0, 1000), (0, 1000), (0, 1000), (20, 1000)]


def _bands(tmp_path):
    path = tmp_path / "bands.yaml"
    path.write_text(BANDS, encoding="utf-8")
    return path


def _metrics(tmp_path, rows):
    lines = [HEADER]
    lines += [f"{i + 1},{echecs},{total},\n" for i, (echecs, total) in enumerate(rows)]
    path = tmp_path / "metrics.csv"
    path.write_text("".join(lines), encoding="utf-8")
    return path


def test_relevé_ordinaire_natteint_aucun_palier(tmp_path):
    rows = REFERENCE_ROWS + [(0, 1000)]
    metrics = _metrics(tmp_path, rows)

    result = detect(metrics, _bands(tmp_path))

    assert result["tier"] == 0
    assert result["action"] is None


def test_relevé_qui_depasse_trois_ecarts_types_atteint_le_palier_3(tmp_path):
    rows = REFERENCE_ROWS + [(50, 1000)]
    metrics = _metrics(tmp_path, rows)

    result = detect(metrics, _bands(tmp_path))

    assert result["tier"] == 3
    assert result["action"] == "propose"


def test_relevé_qui_depasse_tout_juste_un_seuil_natteint_pas_le_palier_du_dessus(tmp_path):
    rows = REFERENCE_ROWS + [(13, 1000)]
    metrics = _metrics(tmp_path, rows)

    result = detect(metrics, _bands(tmp_path))

    assert 1 <= result["deviation"] < 2
    assert result["tier"] == 1
    assert result["action"] == "log"


def test_ligne_du_jour_sans_test_execute_ne_fait_pas_echouer_et_nalerte_pas(tmp_path):
    rows = REFERENCE_ROWS + [(0, 0)]
    metrics = _metrics(tmp_path, rows)

    result = detect(metrics, _bands(tmp_path))

    assert result["tier"] == 0
    assert result["action"] is None


def test_ligne_du_jour_avec_valeur_illisible_ne_fait_pas_echouer_et_nalerte_pas(tmp_path):
    lines = [HEADER]
    lines += [f"{i + 1},{echecs},{total},\n" for i, (echecs, total) in enumerate(REFERENCE_ROWS)]
    lines.append("6,erreur,1000,\n")
    metrics = tmp_path / "metrics.csv"
    metrics.write_text("".join(lines), encoding="utf-8")

    result = detect(metrics, _bands(tmp_path))

    assert result["tier"] == 0
    assert result["action"] is None


def test_ligne_illisible_dans_la_reference_ne_fait_pas_echouer(tmp_path):
    lines = [HEADER]
    lines.append("1,0,1000,\n")
    lines.append("2,erreur,1000,\n")
    lines.append("3,0,1000,\n")
    lines.append("4,0,0,\n")
    lines.append("5,0,1000,\n")
    lines.append("6,0,1000,\n")
    metrics = tmp_path / "metrics.csv"
    metrics.write_text("".join(lines), encoding="utf-8")

    result = detect(metrics, _bands(tmp_path))

    assert result["tier"] == 0
