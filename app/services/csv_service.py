import pandas as pd


def extract_text(path: str) -> str:
    """
    Extract text from a CSV file and convert rows
    into structured sentences suitable for RAG.
    """

    df = pd.read_csv(path)

    rows = []

    for _, row in df.iterrows():

        row_text = " | ".join(
            f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])
        )

        rows.append(row_text)

    return "\n".join(rows)