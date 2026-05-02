from data_analysis_M3 import load_collated_data, generate_means_sequence, visualize_data

file_path = "output/collated_answers.txt"

data = load_collated_data(file_path)
means = generate_means_sequence(file_path)

print("Number of respondents:")
print(len(data))

print("Number of questions:")
print(len(means))

print("First 10 mean values:")
print(means[:10])

visualize_data(file_path, 1)
visualize_data(file_path, 2)
visualize_data(file_path, 3)