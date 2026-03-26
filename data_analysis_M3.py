import os
import matplotlib.pyplot as plt

def load_collated_answers(collated_answers_path):
    if not os.path.exists(collated_answers_path):
        raise FileNotFoundError(f"File not found: {collated_answers_path}")

    data = []

    with open(collated_answers_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "," in line:
            parts = line.split(",")
        else:
            parts = line.split()
        row = [int(x) for x in parts]
        data.append(row)

    if len(data) == 0:
        raise ValueError("Empty data")

    row_length = len(data[0])
    for row in data:
        if len(row) != row_length:
            raise ValueError("Inconsistent row length")

    return data


def generate_means_sequence(collated_answers_path):
    data = load_collated_answers(collated_answers_path)
    num_questions = len(data[0])
    means = []

    for q in range(num_questions):
        column_values = [row[q] for row in data]
        valid_answers = [x for x in column_values if x != 0]

        if len(valid_answers) == 0:
            mean_value = 0
        else:
            mean_value = sum(valid_answers) / len(valid_answers)

        means.append(mean_value)

    return means


def visualize_data(collated_answers_path, n):
    means = generate_means_sequence(collated_answers_path)
    question_numbers = list(range(1, len(means) + 1))

    if n == 1:
        plt.scatter(question_numbers, means)
        plt.xlabel("Question")
        plt.ylabel("Mean")
        plt.title("Scatter Plot")
        plt.show()

    elif n == 2:
        plt.plot(question_numbers, means, marker="o")
        plt.xlabel("Question")
        plt.ylabel("Mean")
        plt.title("Line Plot")
        plt.show()

    else:
        print("Error")


def main():
    collated_answers_path = "collated_answers.txt"
    means = generate_means_sequence(collated_answers_path)
    print(means)
    visualize_data(collated_answers_path, 1)
    visualize_data(collated_answers_path, 2)


if __name__ == "__main__":
    main()

