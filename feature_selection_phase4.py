"""Training-only Phase 4 feature selection evidence.

This is an analytical instrument, not final model selection. It reads the
full raw source, uses only 2021-2024 development rows, and writes small
feature-level reports. No model or processed dataset is persisted.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from sklearn.tree import DecisionTreeClassifier

from prepare_phase3 import (
    CATEGORICAL_FEATURES,
    CLASSIFICATION_FEATURES,
    DATA_PATH,
    NUMERIC_FEATURES,
    TARGET,
    build_preprocessor,
)


RANDOM_STATE = 42
ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
SUMMARY_PATH = RESULTS_DIR / "feature_selection_summary.csv"
REDUNDANCY_PATH = RESULTS_DIR / "feature_selection_redundancy.csv"
METADATA_PATH = RESULTS_DIR / "feature_selection_metadata.json"


def load_development() -> tuple[pd.DataFrame, pd.Series]:
    raw = pd.read_csv(DATA_PATH, low_memory=False)
    data = raw[raw["collision_year"] <= 2024].copy().reset_index(drop=True)
    data["month"] = pd.to_datetime(data["date"], format="%d/%m/%Y", errors="raise").dt.month
    data["hour"] = pd.to_datetime(data["time"], format="%H:%M", errors="raise").dt.hour
    x = data[CLASSIFICATION_FEATURES].copy()
    for column in CATEGORICAL_FEATURES:
        x[column] = x[column].astype("string")
    return x, data[TARGET].copy()


def mutual_information_by_feature(x: pd.DataFrame, y: pd.Series) -> dict[str, float]:
    scores: dict[str, float] = {}
    for feature in CLASSIFICATION_FEATURES:
        values = x[feature].fillna("__MISSING__") if feature in CATEGORICAL_FEATURES else x[feature]
        encoded = pd.factorize(values, sort=True)[0] if feature in CATEGORICAL_FEATURES else values.to_numpy()
        score = mutual_info_classif(
            encoded.reshape(-1, 1), y, discrete_features=True, random_state=RANDOM_STATE
        )[0]
        scores[feature] = float(score)
    return scores


def stability_by_year(x: pd.DataFrame, y: pd.Series) -> dict[str, float]:
    values: dict[str, list[float]] = {feature: [] for feature in CLASSIFICATION_FEATURES}
    years = pd.read_csv(DATA_PATH, usecols=["collision_year"])["collision_year"]
    development_years = years[years <= 2024].reset_index(drop=True)
    for year in sorted(development_years.unique()):
        mask = development_years == year
        for feature in CLASSIFICATION_FEATURES:
            feature_values = x.loc[mask, feature]
            encoded = pd.factorize(feature_values.fillna("__MISSING__"), sort=True)[0]
            values[feature].append(float(mutual_info_classif(
                encoded.reshape(-1, 1), y.loc[mask], discrete_features=True, random_state=RANDOM_STATE
            )[0]))
    return {feature: float(max(scores) - min(scores)) for feature, scores in values.items()}


def main() -> None:
    x, y = load_development()
    mi_scores = mutual_information_by_feature(x, y)
    stability_range = stability_by_year(x, y)

    preprocessor = build_preprocessor()
    encoded = preprocessor.fit_transform(x)
    instrument = DecisionTreeClassifier(
        max_depth=8, min_samples_leaf=100, class_weight="balanced", random_state=RANDOM_STATE
    )
    instrument.fit(encoded, y)
    names = preprocessor.get_feature_names_out()
    tree_scores = {feature: 0.0 for feature in CLASSIFICATION_FEATURES}
    for name, importance in zip(names, instrument.feature_importances_):
        matches = [
            feature for feature in CLASSIFICATION_FEATURES
            if name == f"numeric__{feature}" or name.startswith(f"categorical__{feature}_")
        ]
        if matches:
            tree_scores[matches[0]] += float(importance)

    summary = pd.DataFrame({
        "feature": CLASSIFICATION_FEATURES,
        "mutual_information": [mi_scores[f] for f in CLASSIFICATION_FEATURES],
        "tree_importance_aggregated": [tree_scores[f] for f in CLASSIFICATION_FEATURES],
        "yearly_mi_range_2021_2024": [stability_range[f] for f in CLASSIFICATION_FEATURES],
        "selection_status": "provisional_core",
    }).sort_values(["tree_importance_aggregated", "mutual_information"], ascending=False)

    redundancy = pd.DataFrame([
        {"feature_a": "date", "feature_b": "month", "issue": "derived representation overlap", "action": "use month; exclude raw date"},
        {"feature_a": "time", "feature_b": "hour", "issue": "derived representation overlap", "action": "use hour; exclude raw time"},
        {"feature_a": "location_easting_osgr", "feature_b": "longitude", "issue": "alternative geographic representations", "action": "review at most one representation"},
        {"feature_a": "location_northing_osgr", "feature_b": "latitude", "issue": "alternative geographic representations", "action": "review at most one representation"},
        {"feature_a": "local_authority_highway", "feature_b": "local_authority_highway_current", "issue": "possible versioned administrative overlap", "action": "confirm definitions before selection"},
    ])
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUMMARY_PATH, index=False)
    redundancy.to_csv(REDUNDANCY_PATH, index=False)
    metadata = {
        "phase": "4", "rows_used": int(len(x)), "years_used": [2021, 2022, 2023, 2024],
        "test_year_used": False, "target_used_as_input": False, "random_state": RANDOM_STATE,
        "instrument": "DecisionTreeClassifier(max_depth=8, min_samples_leaf=100, class_weight=balanced)",
        "encoded_feature_count": int(encoded.shape[1]),
        "outputs": [str(path.relative_to(ROOT)).replace("\\", "/") for path in [SUMMARY_PATH, REDUNDANCY_PATH, METADATA_PATH]],
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(summary.to_string(index=False))
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
