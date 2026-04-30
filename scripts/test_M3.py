from data_analysis_M3 import generate_means_sequence, visualize_data

file_path = "output/collated_answers.txt"

means = generate_means_sequence(file_path)

print("Mean sequence:")
print(means)

print("Number of questions:")
print(len(means))

visualize_data(file_path, 1)
visualize_data(file_path, 2)
visualize_data(file_path, 3)