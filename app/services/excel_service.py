import pandas as pd


def extract_text(path: str) -> str:
    """
    Extract structured text from all sheets in an Excel file.
    Returns formatted text suitable for embeddings and RAG.
    """

    try:
        sheets = pd.read_excel(path, sheet_name=None)

        full_text = []

        for sheet_name, df in sheets.items():

            full_text.append(f"===== Sheet: {sheet_name} =====")

            # Replace NaN values
            df = df.fillna("")

            # Convert rows into key-value structure
            for _, row in df.iterrows():

                row_text = " | ".join(
                    f"{col}: {row[col]}" for col in df.columns if str(row[col]).strip()
                )

                if row_text:
                    full_text.append(row_text)

        return "\n".join(full_text)

    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")