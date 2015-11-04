import project_config
import kmeans

import nibabel as nib

"""
Replace these variables before running the script
"""
BOLD_file_1 = 'bold_1.nii.gz'
BOLD_file_2 = 'bold_2.nii.gz'
BOLD_file_3 = 'bold_3.nii.gz'


img_1 = nib.load(BOLD_file_1)
data_1 = img_1.get_data()
data_1 = data_1[..., 4:]

img_2 = nib.load(BOLD_file_2)
data_2 = img_2.get_data()
data_2 = data_2[..., 4:]

img_3 = nib.load(BOLD_file_3)
data_3 = img_3.get_data()
data_3 = data_3[..., 4:]

n_clusters = 5

labels_1 = kmeans.perform_kMeans_clustering_analysis(data_1, n_clusters)
labels_2 = kmeans.perform_kMeans_clustering_analysis(data_2, n_clusters)
labels_3 = kmeans.perform_kMeans_clustering_analysis(data_3, n_clusters)

labels_list = [labels_1, labels_2, labels_3]
shape = data_1.shape

result_labels = kmeans.merge_n_clusters(labels_list, n_clusters, shape[:-1])