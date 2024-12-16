import pandas as pd


def transform_csv(input_file, output_file):
    """
    Transforms the input CSV file into the desired format with calculated levels and updates columns.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the transformed CSV file.
    """
    try:
        # Load the CSV file
        df = pd.read_csv(input_file)

        # Define a function to determine the score based on the level
        def determine_score(level):
            if level == "easy":
                return 5
            elif level == "medium":
                return 10
            elif level == "hard":
                return 15
            else:
                return None

        # Transform the columns
        df["origin_id"] = df["file_name"]
        df["source"] = df["uni"]
        df["target"] = df["url"]  # Set target to empty string
        df["score"] = df["level"].apply(determine_score)
        df["target_dialect"] = "U-tsang"  # Set target_dialect to empty string
        df["source_language"] = "Tibetan"
        df["target_language"] = "Tibetan"

        # Select the required columns
        transformed_df = df[
            [
                "origin_id",
                "source",
                "target",
                "score",
                "target_dialect",
                "source_language",
                "target_language",
            ]
        ]

        # Save the transformed DataFrame to a new CSV file
        transformed_df.to_csv(output_file, index=False)

        print(
            f"Transformed CSV saved to {output_file}. Total rows: {len(transformed_df)}"
        )
    except Exception as e:
        print(f"Error while transforming CSV: {e}")


# Example usage
input_csv = "data/validation/pema_updated_file.csv"  # Replace with your input file path
output_csv = "data/validation/pema_transformed_file.csv"  # Replace with your desired output file path

transform_csv(input_csv, output_csv)
