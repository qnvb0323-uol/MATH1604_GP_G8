from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt


def load_collated_data(collated_answers_path):
    """
    Read collated_answers.txt and convert it into answer sequences.
    Each respondent should have 100 answers.
    """
    path = Path(collated_answers_path)

    if not path.exists():
        raise FileNotFoundError(f"Cannot find file: {path}")

    text = path.read_text(encoding="utf-8").strip()

    if not text:
        raise ValueError("The collated answers file is empty.")

    # Split respondents (line containing only "*")
    respondent_sections = [
        section.strip()
        for section in re.split(r"(?m)^\s*\*\s*$", text)
        if section.strip()
    ]

    all_sequences = []

    for respondent_number, section in enumerate(respondent_sections, start=1):
        question_blocks = re.split(r"\n(?=Question\s+\d+\.)", section)

        sequence = []

        for block in question_blocks:
            block = block.strip()

            if not block.startswith("Question"):
                continue

            option_number = 0
            selected_answer = 0

            for line in block.splitlines():
                line = line.strip()

                if line.startswith("["):
                    option_number += 1

                    if re.match(r"^\[\s*[xX]\s*\]", line):
                        selected_answer = option_number

            sequence.append(selected_answer)
        # Ensure exactly 100 answers
        if len(sequence) != 100:
            raise ValueError(
                f"Respondent {respondent_number}: expected 100 answers, "
                f"but found {len(sequence)}."
            )

        all_sequences.append(sequence)

    return all_sequences


def generate_means_sequence(collated_answers_path):
    """
    Compute mean answer value for each question.
    Ignore unanswered (0) values.
    """
    data = load_collated_data(collated_answers_path)
    data_array = np.array(data)

    means = []

    for question_index in range(data_array.shape[1]):
        question_answers = data_array[:, question_index]

        valid_answers = question_answers[question_answers != 0]

        if len(valid_answers) == 0:
            means.append(float("nan"))
        else:
            means.append(float(np.mean(valid_answers)))

    return means


def visualize_data(collated_answers_path, n):
    """
    Visualise results:
    n = 1 → scatter plot (mean values)
    n = 2 → line plot (individual + mean)
    """
    data = load_collated_data(collated_answers_path)
    data_array = np.array(data)
    means = generate_means_sequence(collated_answers_path)

    question_numbers = range(1, len(means) + 1)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    plt.figure(figsize=(10, 6))

    if n == 1:
        plt.scatter(question_numbers, means)
        plt.title("Scatter Plot of Mean Answer Values")
        plt.xlabel("Question Number")
        plt.ylabel("Mean Answer Value")
        plt.grid(True)
        plt.savefig(output_dir / "scatter_plot_M3.png", dpi=300, bbox_inches="tight")
        print("Scatter plot saved to output/scatter_plot_M3.png")

    elif n == 2:
        for respondent_answers in data_array:
            plt.plot(question_numbers, respondent_answers, alpha=0.25)

        plt.plot(question_numbers, means, linewidth=2.5, label="Mean answer value")
        plt.title("Line Plot of Individual Answers and Mean Sequence")
        plt.xlabel("Question Number")
        plt.ylabel("Answer Value")
        plt.legend()
        plt.grid(True)
        plt.savefig(output_dir / "line_plot_M3.png", dpi=300, bbox_inches="tight")
        print("Line plot saved to output/line_plot_M3.png")

    else:
        print("Error: n must be 1 for a scatter plot or 2 for a line plot.")
        return

    plt.show()
    plt.close()