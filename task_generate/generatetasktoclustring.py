# Given that the output got truncated previously, I'll remove the print statements for simulation and focus on the code structure.
# Re-running the corrected code for task simulation, golden standard calculation, and clustering.

from collections import defaultdict
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import random
from collections import Counter
import pandas as pd


class Worker:
    def __init__(self, name):
        self.name = name
        self.selected_addresses = []

# Validation function


def validate_input(selected, task):
    if len(selected) != 3:
        return False, "You must select exactly 3 addresses."
    if len(set(selected)) != len(selected):
        return False, "Duplicate selections are not allowed."
    for address in selected:
        if address not in task:
            return False, f"The address {address} is not in the task list."
    return True, ""


# CSVファイルを読み込む
file_path = 'GR03_contributions.csv'
df = pd.read_csv(file_path)

# 'address' カラムの重複を削除
df_unique = df.drop_duplicates(subset=['address'])

# 最初の100個のウォレットアドレスを取得
wallet_addresses = df_unique['address'].head(100).tolist()

# Generate initial tasks
initial_tasks = [wallet_addresses[i:i+6]
                 for i in range(0, len(wallet_addresses), 6)]
print("initial_tasks")
print(initial_tasks)

# Create worker instances
workers = [Worker(f'Worker_{i}') for i in range(1, 4)]

# Placeholder for subsequent tasks
subsequent_tasks = []

# Placeholder for all selected addresses
all_selected_addresses = []

# Simulate 2 rounds of task assignment, completion, and golden standard calculation
for round_num in range(1, 3):
    for worker in workers:
        for task in initial_tasks:
            while True:
                # ‼️ Simulated worker input for task completion. Replace this with actual input.
                selected = random.sample(task, 3)

                is_valid, message = validate_input(selected, task)
                if is_valid:
                    worker.selected_addresses.extend(selected)
                    all_selected_addresses.extend(selected)

                    break

        # Calculate golden standards based on workers' selections and generate subsequent tasks
        address_count = Counter(worker.selected_addresses)
        golden_standard = address_count.most_common(1)[0][0]
        worker.selected_addresses = []  # Clear selections for the next round

        # Generate new task based on the golden standard
        index = wallet_addresses.index(golden_standard)
        next_task = wallet_addresses[max(0, index - 2):index + 4]
        if len(next_task) < 6:
            next_task.extend(wallet_addresses[:6 - len(next_task)])
        subsequent_tasks.append(next_task)
        print("subsequent_tasks")
        print(subsequent_tasks)

    # Update initial tasks for the next round
    initial_tasks = subsequent_tasks.copy()
    subsequent_tasks = []

# # Prepare data for clustering
# address_vectors = {address: [random.uniform(0, 1) for _ in range(
#     5)] for address in set(all_selected_addresses)}
# data_for_pca = [address_vectors[address] for address in all_selected_addresses]

# # Perform PCA and clustering
# pca = PCA(n_components=2)
# transformed_data = pca.fit_transform(data_for_pca)
# # `n_clusters` means, how many make cluster
# kmeans = KMeans(n_clusters=5)
# clusters = kmeans.fit_predict(transformed_data)

# # Display clustering results
# clustered_addresses = {i: [] for i in range(max(clusters) + 1)}
# for i, cluster_id in enumerate(clusters):
#     clustered_addresses[cluster_id].append(all_selected_addresses[i])

# for cluster_id in clustered_addresses:
#     clustered_addresses[cluster_id] = list(
#         set(clustered_addresses[cluster_id]))

# print("\nCluster Analysis:")
# for cluster, addresses in clustered_addresses.items():
#     print(f"Cluster {cluster}:")
#     for i, address in enumerate(addresses):
#         print(f"  - {address}")


# def find_multiple_cluster_addresses(clustered_addresses):
#     address_to_clusters = defaultdict(list)
#     for cluster_id, addresses in clustered_addresses.items():
#         for address in addresses:
#             address_to_clusters[address].append(cluster_id)

#     # Filter out addresses that belong to multiple clusters
#     multiple_cluster_addresses = {address: clusters for address,
#                                   clusters in address_to_clusters.items() if len(clusters) > 1}
#     return multiple_cluster_addresses


# print(find_multiple_cluster_addresses(clustered_addresses))


# ---

# Prepare data for clustering
address_vectors = {address: [random.uniform(0, 1) for _ in range(
    5)] for address in set(all_selected_addresses)}

# Add a small random noise to simulate real-world data
address_vectors = {address: [x + random.uniform(-0.05, 0.05) for x in vec]
                   for address, vec in address_vectors.items()}

data_for_pca = [address_vectors[address] for address in all_selected_addresses]

# Perform PCA and clustering
pca = PCA(n_components=2)
transformed_data = pca.fit_transform(data_for_pca)

# Run K-means multiple times and merge the results
merged_clusters = defaultdict(set)
for _ in range(3):  # Run K-means 3 times
    kmeans = KMeans(n_clusters=5)
    clusters = kmeans.fit_predict(transformed_data)
    for i, cluster_id in enumerate(clusters):
        merged_clusters[all_selected_addresses[i]].add(cluster_id)

# Display results
print("\nCluster Analysis:")
for address, cluster_ids in merged_clusters.items():
    print(f"{address} belongs to clusters {list(cluster_ids)}")
