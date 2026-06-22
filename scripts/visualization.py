"""
Visualization helpers for the Experience-Centered AI analysis.

Charts are saved to the charts/ folder so they can be reused in the
README, report, and final portfolio presentation.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_company_ranking_chart(
    df: pd.DataFrame,
    chart_dir: Path,
    filename: str = "company_rankings.png",
) -> None:
    """
    Create and save a horizontal bar chart of company Experience AI scores.
    """

    ranked = df.sort_values(
        "experience_ai_score",
        ascending=True
    )

    plt.figure(figsize=(12, 6))

    plt.barh(
        ranked["company"],
        ranked["experience_ai_score"]
    )

    # Add score labels to bars
    for i, score in enumerate(ranked["experience_ai_score"]):
        plt.text(
            score + 0.05,
            i,
            f"{score:.2f}",
            va="center"
        )

    plt.xlabel("Experience AI Score")
    plt.ylabel("Company")
    plt.title("Experience-Centered AI Company Rankings")
    plt.xlim(0, 10)

    plt.tight_layout()

    chart_path = chart_dir / filename

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


def save_industry_ranking_chart(
    df: pd.DataFrame,
    chart_dir: Path,
    filename: str = "industry_rankings.png",
) -> pd.DataFrame:
    """
    Create and save a horizontal bar chart of average industry scores.
    """

    industry_scores = (
        df.groupby("industry", as_index=False)["experience_ai_score"]
        .mean()
        .sort_values("experience_ai_score", ascending=True)
    )

    plt.figure(figsize=(10, 5))

    plt.barh(
        industry_scores["industry"],
        industry_scores["experience_ai_score"]
    )

    # Add score labels
    for i, score in enumerate(industry_scores["experience_ai_score"]):
        plt.text(
            score + 0.05,
            i,
            f"{score:.2f}",
            va="center"
        )

    plt.xlabel("Average Experience AI Score")
    plt.ylabel("Industry")
    plt.title("Experience-Centered AI Industry Rankings")
    plt.xlim(0, 10)

    plt.tight_layout()

    chart_path = chart_dir / filename

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    return industry_scores


def save_sensitivity_chart(
    sensitivity_summary: pd.DataFrame,
    chart_dir: Path,
    filename: str = "ranking_stability.png",
) -> None:
    """
    Create and save a chart showing how often each company
    appears in the Top 3 during Monte Carlo simulations.
    """

    ranked = sensitivity_summary.sort_values(
        "top_3_frequency",
        ascending=True
    )

    plt.figure(figsize=(12, 6))

    plt.barh(
        ranked["company"],
        ranked["top_3_frequency"]
    )

    # Add percentage labels
    for i, score in enumerate(ranked["top_3_frequency"]):
        plt.text(
            score + 0.01,
            i,
            f"{score:.1%}",
            va="center"
        )

    plt.xlabel("Top 3 Frequency")
    plt.ylabel("Company")
    plt.title("Ranking Stability Analysis (10,000 Simulations)")
    plt.xlim(0, 1)

    plt.tight_layout()

    chart_path = chart_dir / filename

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()