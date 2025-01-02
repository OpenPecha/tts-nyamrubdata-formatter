import csv
import os
import re

from row_remover_based_on_selected_id import should_ignore


def preprocess_text(text):
    """
    Clean up the text and normalize Tibetan punctuation patterns,
    treating ༄༅། the same as ༄༅།།
    Args:
        text (str): Input Tibetan text.

    Returns:
        str: Cleaned and normalized text
    """
    # First normalize ༄༅། to ༄༅།།
    text = re.sub(r"༄༅།(?!།)", "༄༅།།", text)
    # Remove extra whitespace but preserve single spaces
    text = " ".join(text.split())
    return text


def segment_sentences(text):
    """
    Segment text into sentences based on shey markers (། or །།),
    treating ༄༅། the same as ༄༅།།
    Args:
        text (str): Input Tibetan text.

    Returns:
        list: A list of segmented sentences
    """
    # First, preprocess the text
    text = preprocess_text(text)

    # Split by shey markers while preserving them
    segments = re.split(r"(།།|།(?!།))", text)

    # Combine segments with their respective shey markers
    full_segments = []
    current_segment = ""

    i = 0
    while i < len(segments):
        segment = segments[i].strip()

        # Get the shey marker (if any)
        shey = ""
        if i + 1 < len(segments) and segments[i + 1]:
            shey = segments[i + 1]
            i += 2
        else:
            i += 1

        if segment:
            # Check if segment contains ༄༅།། (including normalized ༄༅།)
            is_yigchung = bool(re.search(r"༄༅།།?", segment))

            if is_yigchung:
                # If we have a current segment, add it to results
                if current_segment:
                    full_segments.append(current_segment)
                current_segment = segment + shey
            else:
                # For normal text, append to current segment
                if current_segment:
                    current_segment = current_segment + " " + segment + shey
                else:
                    current_segment = segment + shey

            # If this segment ends with ། or །།, add it to results
            if shey and not is_yigchung:
                full_segments.append(current_segment)
                current_segment = ""

    # Handle any remaining segment
    if current_segment:
        full_segments.append(current_segment)

    # Post-process: ensure yigchung segments are properly combined
    processed_segments = []
    i = 0
    while i < len(full_segments):
        segment = full_segments[i].strip()

        # If this segment contains ༄༅། or ༄༅།།, combine it with the next segment
        if re.search(r"༄༅།།?", segment) and i + 1 < len(full_segments):
            processed_segments.append(f"{segment} {full_segments[i+1]}")
            i += 2
        else:
            processed_segments.append(segment)
            i += 1

    return processed_segments


def create_csv_with_corrected_segments(etext_folder, output_csv):
    """
    Create a CSV file with segmented sentences from e-text files.
    Args:
        etext_folder (str): Path to the folder containing e-text files.
        output_csv (str): Path to the output CSV file.
    """

    rows = []
    for file in os.listdir(etext_folder):
        if file.endswith(".txt"):
            file_id = os.path.splitext(file)[0]

            # Check if the file should be ignored
            if should_ignore(file_id):
                print(f"Ignoring file: {file}")
                continue

            file_path = os.path.join(etext_folder, file)

            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Segment sentences with the updated rules
            sentences = segment_sentences(content)

            # Generate rows with file_name and segmented sentences
            for idx, sentence in enumerate(sentences, start=1):
                file_name = f"{file_id}_{str(idx).zfill(5)}"
                rows.append([file_name, sentence])

    # Write to CSV
    with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file_name", "etext_transcript"])  # Write header
        writer.writerows(rows)

    print(f"CSV file created successfully at: {output_csv}")


# Example usage:
etext_folder = "data/etexts"  # Replace with the path to your e-text folder
output_csv = "output_etext_transcripts.csv"  # Replace with your desired output CSV path
create_csv_with_corrected_segments(etext_folder, output_csv)
