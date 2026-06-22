"""
Utility functions for the Experience-Centered AI scoring model.

This file contains reusable scoring and sensitivity-analysis functions.
Keeping this logic outside notebooks makes the project cleaner and easier
to explain in a portfolio or interview.
"""

import numpy as np
import pandas as pd


FACTOR_COLUMNS = [
    "experience_intensity",
    "ai_enhancement",
    "repeat_usage",
    "agency_preservation",
    "revenue_capture",
    "network_effects",
]


BASE_WEIGHTS = {
    "experience_intensity": 0.25,
    "ai_enhancement": 0.20,
    "repeat_usage": 0.20,
    "agency_preservation": 0.15,
    "revenue_capture": 0.10,
    "network_effects": 0.10,
}


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names for consistent analysis.
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    return df


def calculate_weighted_score(
    df: pd.DataFrame,
    weights: dict = BASE_WEIGHTS,
    score_name: str = "python_score",
) -> pd.DataFrame:
    """
    Calculate a weighted Experience AI score from factor columns.
    """
    df = df.copy()

    df[score_name] = sum(df[col] * weight for col, weight in weights.items())

    return df


def run_monte_carlo_sensitivity(
    df: pd.DataFrame,
    factor_columns: list = FACTOR_COLUMNS,
    n_simulations: int = 10000,
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    Run Monte Carlo sensitivity analysis by randomly generating scoring weights.

    Each simulation creates a random set of weights that sum to 1.
    The function returns company rank results across all simulations.
    """
    np.random.seed(random_seed)

    results = []

    scores = df[factor_columns].to_numpy()
    companies = df["company"].to_numpy()

    for i in range(n_simulations):
        weights = np.random.dirichlet(np.ones(len(factor_columns)))
        simulated_scores = scores @ weights

        temp = pd.DataFrame({
            "simulation": i + 1,
            "company": companies,
            "simulated_score": simulated_scores,
        })

        temp["rank"] = temp["simulated_score"].rank(
            ascending=False,
            method="min"
        )

        results.append(temp)

    return pd.concat(results, ignore_index=True)


def summarize_sensitivity(sim_results: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize Monte Carlo ranking stability by company.
    """
    summary = (
        sim_results
        .groupby("company")
        .agg(
            average_rank=("rank", "mean"),
            median_rank=("rank", "median"),
            best_rank=("rank", "min"),
            worst_rank=("rank", "max"),
            top_3_frequency=("rank", lambda x: (x <= 3).mean()),
            average_score=("simulated_score", "mean"),
        )
        .reset_index()
        .sort_values("average_rank")
    )

    return summary