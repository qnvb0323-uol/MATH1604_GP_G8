import numpy as np
import matplotlib.pyplot as plt


def load_collated_data(collated_answers_path):
    data = []

    with open(collated_answers_path, "r") as file:
        for line in file:
            line = line.strip()

            if line == "" or line == "*":
                continue

            answers = [int(value) for value in line.split()]
            data.append(answers)

    if len(data) == 0:
        raise ValueError("The collated answers file is empty or contains no valid answer rows.")

    row_lengths = [len(row) for row in data]
    if len(set(row_lengths)) != 1:
        raise ValueError("All respondent answer sequences must have the same length.")

    return data


def generate_means_sequence(collated_answers_path):

    data = load_collated_data(collated_answers_path)
    data_array = np.array(data)

    means = []

    for question_index in range(data_array.shape[1]):
        question_answers = data_array[:, question_index]

        # Exclude unanswered questions coded as 0
        valid_answers = question_answers[question_answers != 0]

        if len(valid_answers) == 0:
            means.append(float("nan"))
        else:
            means.append(float(np.mean(valid_answers)))

    return means


def visualize_data(collated_answers_path, n):

    data = load_collated_data(collated_answers_path)
    data_array = np.array(data)
    means = generate_means_sequence(collated_answers_path)

    question_numbers = range(1, len(means) + 1)

    plt.figure(figsize=(10, 6))

    if n == 1:
        plt.scatter(question_numbers, means)
        plt.title("Scatter Plot of Mean Answer Values")
        plt.xlabel("Question Number")
        plt.ylabel("Mean Answer Value")
        plt.grid(True)
        plt.savefig("output/scatter_plot_M3.png", dpi=300, bbox_inches="tight")
        print("Scatter plot saved to output/scatter_plot_M3.png")

    elif n == 2:
        for respondent_answers in data_array:
            plt.plot(question_numbers, respondent_answers, alpha=0.3)

        plt.plot(question_numbers, means, linewidth=2.5, label="Mean answer value")
        plt.title("Line Plot of Individual Answers and Mean Sequence")
        plt.xlabel("Question Number")
        plt.ylabel("Answer Value")
        plt.legend()
        plt.grid(True)
        plt.savefig("output/line_plot_M3.png", dpi=300, bbox_inches="tight")
        print("Line plot saved to output/line_plot_M3.png")

    else:
        print("Error: n must be 1 for a scatter plot or 2 for a line plot.")
        return

    plt.show()
    plt.close()
