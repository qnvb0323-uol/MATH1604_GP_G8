from data_analysis_M3 import generate_means_sequence, visualize_data

file_path = "output/collated_answers.txt"

means = generate_means_sequence(file_path)
print(means)

visualize_data(file_path, 1)
visualize_data(file_path, 2)