from pathlib import Path
import sys
import importlib.util
import importlib.machinery


BASE_URL = "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"
NUMBER_OF_RESPONDENTS = 64


def load_m2_module():
    """
    Load the compiled M2 module from the correct .pyc file.

    The .pyc file depends on the Python version.
    For example, Python 3.12 uses data_preparation_M2.cpython-312.pyc.
    """
    version_tag = f"{sys.version_info.major}{sys.version_info.minor}"

    possible_paths = [
        Path(f"scripts/__pycache__/data_preparation_M2.cpython-{version_tag}.pyc"),
        Path(f"data_preparation_M2.cpython-{version_tag}.pyc"),
        Path("scripts/data_preparation_M2.pyc"),
    ]

    pyc_path = None

    for path in possible_paths:
        if path.exists():
            pyc_path = path
            break

    if pyc_path is None:
        raise FileNotFoundError(
            f"Cannot find data_preparation_M2.cpython-{version_tag}.pyc. "
            f"Your Python version is {sys.version_info.major}.{sys.version_info.minor}. "
            "Make sure the correct M2 .pyc file is placed in scripts/__pycache__/."
        )

    print(f"Using M2 file: {pyc_path}")

    loader = importlib.machinery.SourcelessFileLoader(
        "data_preparation_M2",
        str(pyc_path)
    )

    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)

    return module


def main():
    """
    Run the M2 data preparation process using the professor-provided .pyc file.

    This script downloads raw answer files and creates output/collated_answers.txt.
    """
    data_folder = Path("data")
    output_folder = Path("output")

    data_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)

    m2 = load_m2_module()

    if not hasattr(m2, "download_answer_files"):
        raise AttributeError("M2 module does not contain download_answer_files().")

    if not hasattr(m2, "collate_answer_files"):
        raise AttributeError("M2 module does not contain collate_answer_files().")

    print("\nDownloading raw answer files...")

    for respondent_index in range(1, NUMBER_OF_RESPONDENTS + 1):
        try:
            m2.download_answer_files(
                BASE_URL,
                str(data_folder),
                respondent_index
            )
            print(f"Downloaded respondent {respondent_index}")

        except Exception as error:
            print(f"Failed to download respondent {respondent_index}: {error}")

    print("\nCollating answer files...")

    result = m2.collate_answer_files(str(data_folder))

    output_path = output_folder / "collated_answers.txt"

    # Some versions of collate_answer_files may return the collated text
    # instead of writing it directly to a file.
    if isinstance(result, str):
        output_path.write_text(result, encoding="utf-8")
        print(f"Saved returned text to {output_path}")

    print("\nChecking output...")

    if output_path.exists():
        print(f"Success: {output_path} has been created.")
    else:
        print("collated_answers.txt was not found in output/.")
        print("Searching for any collated_answers.txt file in the project...")

        matches = list(Path(".").rglob("collated_answers.txt"))

        if matches:
            print("Found:")
            for match in matches:
                print(match)
        else:
            print("No collated_answers.txt file was found.")


if __name__ == "__main__":
    main()