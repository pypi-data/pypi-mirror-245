import json
import logging
import sys
import numpy as np
import pandas as pd
from sentence_transformers import *
from sklearn.neighbors import NearestCentroid
from sklearn.cluster import AgglomerativeClustering
from few_shot_priming.config import *
from few_shot_priming.experiments import *
def get_embeddings(df_training):
    model = SentenceTransformer('all-mpnet-base-v2')
    training_text = df_training["text"]
    topics = df_training["topic"].values.tolist()
    training_embeddings = model.encode(training_text.values.tolist())
    ids = df_training["id"].values.tolist()
    return training_embeddings, ids, topics

def save_embeddings(embeddings, ids, topics, path):
    ids = np.reshape(ids, (len(ids),1))
    vectors_with_ids = np.hstack((ids, embeddings))
    np.savetxt(path+"/embeddings.txt",vectors_with_ids, delimiter=",")
    with open(path+"/topics.json", "w") as file:
        json.dump(topics, file)



def load_embeddings(path):
    vectors = np.genfromtxt(path+"/embeddings.txt", delimiter=",")
    with open(path+"/topics.json", "r") as file:
        topics = json.load(file)
    return vectors[:,1:], np.uint32(vectors[:,0]), topics

def cluster(vectors, ids, count_of_samples_per_cluster, **args):
    clustering = AgglomerativeClustering(**args).fit(vectors)
    labels = clustering.labels_

    clf = NearestCentroid()
    clf.fit(vectors, labels)
    samples = []
    for centriod in clf.centroids_:
        distances = []
        label = clf.predict([centriod])
        cluster_instances = [l==label[0] for l in labels]

        for i, vector in enumerate(vectors):
            if cluster_instances[i]:
                distances.append((i, np.linalg.norm(centriod-vector)))
        distances = sorted(distances, key= lambda element_id: element_id[1])
        if count_of_samples_per_cluster > len(distances):
            count_of_samples_per_cluster = len(distances)
        sampled_indices = [element_id[0] for element_id in distances[:count_of_samples_per_cluster]]
        samples.extend([(ids[sampled_index], labels[sampled_index]) for sampled_index in sampled_indices])

    return labels, samples


def find_diverse_examples(experiment, experiment_type, k, count_of_samples_per_cluster, topic_count=None, logger=None):
    if experiment_type=="validation":
        validate=True
    else:
        validate=False

    log_message(logger, f"clustering on {experiment} {experiment_type} {k} few shots", logging.INFO)
    dataset = load_splits(experiment, oversample=False, validate=validate, topic_count=topic_count)
    df_training = dataset["training"]
    embeddings, ids, topics = get_embeddings(df_training)
    if k > len(df_training):
        k = len(df_training)

    labels, centroid_samples = cluster(embeddings, ids, count_of_samples_per_cluster, n_clusters=k)
    log_message(logger, f"found {len(set(labels))} clusters", logging.INFO)
    centroid_ids = [centroid_sample[0] for centroid_sample in centroid_samples]
    df_diverse= df_training[df_training["id"].isin(centroid_ids)]
    mapping =dict(centroid_samples)
    df_diverse["cluster"] = df_diverse["id"].apply(lambda x: mapping[x])
    return df_diverse


def save_diverse_examples(experiment, experiment_type, ks, count_of_samples_per_cluster,  topic_counts = None, logger=None):
    if topic_counts:
        path = get_diverse_example_path(experiment, experiment_type, topic_counts)

    else:
        path = get_diverse_example_path(experiment, experiment_type, )
    log_message(logger, f"saving to path {path}")
    all_diverse_samples = []
    if topic_counts:
        log_message(logger, f"performing clustering on {list(topic_counts)}")
        assert (len(ks)==1)
        k = ks[0]

        for topic_count in topic_counts:
            log_message(logger, f"performing clustering on  {topic_count}", logging.INFO)
            df_diverse = find_diverse_examples(experiment, experiment_type, k,count_of_samples_per_cluster, topic_count, logger=logger)
            df_diverse["k"] = k
            df_diverse["topic-count"] = topic_count
            all_diverse_samples.append(df_diverse)
    else:
        for k in ks:
            df_diverse = find_diverse_examples(experiment, experiment_type, k, count_of_samples_per_cluster, topic_count=None, logger=logger)
            df_diverse["k"]=k
            all_diverse_samples.append(df_diverse)

    df_all_diverse_examples = pd.concat(all_diverse_samples)

    df_all_diverse_examples.to_csv(path, sep="\t")

def sample_diverse_examples(experiment, experiment_type, k, topic_count=None):
    path = get_diverse_example_path(experiment, experiment_type, topic_count)
    df_diverse_examples = pd.read_csv(path, sep="\t")

    if topic_count:
        df_diverse_examples = df_diverse_examples[df_diverse_examples["topic-count"]==topic_count]

    pro_ratio = {"validation": 340/(340+264), "test":(340+285)/(340+264+285+150)}
    #dataset_size = {"validation": (150+285), "test":(340+264)}
    pro_count = math.floor(k * pro_ratio[experiment_type])
    con_count = k - pro_count

    df_diverse_examples = df_diverse_examples[df_diverse_examples["k"]==k]
    instances = []
    for cluster, df_cluster in df_diverse_examples.groupby("cluster"):
        con_arguments = df_cluster[df_cluster["stance"]==0]
        pro_arguments = df_cluster[df_cluster["stance"]==1]
        if len(con_arguments) and con_count:
            instance = con_arguments.sample(1)
            con_count = con_count -1
        else:
            instance = pro_arguments.sample(1)
        instance["cluster"]=cluster
        instances.append(instance)
    df_examples = pd.concat(instances)
    print(f"found that count of pro arguments {len(df_examples[df_examples['stance']==1])}")
    df_examples.sort_values("topic", inplace=True)
    return df_examples



