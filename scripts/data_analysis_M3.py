import numpy as np
import matplotlib.pyplot as plt


def load_collated_data(path):
    data = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            if line == "" or line == "*":
                continue

            answers = list(map(int, line.split()))
            data.append(answers)

    return data


def generate_means_sequence(collated_answers_path):
    data = load_collated_data(collated_answers_path)

    data = np.array(data)

    means = []

    for i in range(data.shape[1]):
        column = data[:, i]

        # ignore unanswered (0)
        column = column[column != 0]

        if len(column) > 0:
            means.append(np.mean(column))
        else:
            means.append(0)

    return means


def visualize_data(collated_answers_path, n):
    means = generate_means_sequence(collated_answers_path)

    x = range(1, len(means) + 1)

    plt.figure()

    if n == 1:
        plt.scatter(x, means)
        plt.title("Scatter Plot of Mean Answers")
        plt.savefig("output/scatter_plot_M3.png", dpi=300, bbox_inches="tight")
        print("Scatter plot saved to output/scatter_plot_M3.png")

    elif n == 2:
        plt.plot(x, means)
        plt.title("Line Plot of Mean Answers")
        plt.savefig("output/line_plot_M3.png", dpi=300, bbox_inches="tight")
        print("Line plot saved to output/line_plot_M3.png")

    else:
        print("Invalid option. Use n=1 for scatter plot or n=2 for line plot.")
        return

    plt.xlabel("Question Number")
    plt.ylabel("Mean Answer Value")
    plt.grid()
    plt.show()
    plt.close()
