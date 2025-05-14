
# clean the final output
def clean_report(file_path):
    """
    Clean the final output HTML file by removing the first and last lines.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    cleaned_lines = lines[1:-1]
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)