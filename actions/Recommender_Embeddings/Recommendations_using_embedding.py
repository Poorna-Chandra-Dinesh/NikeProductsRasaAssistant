##########################################################################################
##########################################################################################
#
#   Developed by Atef Bader, PhD
#   Last Edit: 11/13/2024
#
#   Description: This a modified script of the original script published on GitHub for OpenAI/Cookbook Repo
#                   Original script availabel at this URL: 
#                   https://github.com/openai/openai-cookbook/blob/main/examples/Recommendation_using_embeddings.ipynb
#
##########################################################################################
##########################################################################################


#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import pickle

from actions.Recommender_Embeddings.utils.embeddings_utils import (
    get_embedding,
    distances_from_embeddings,
    tsne_components_from_embeddings,
    chart_from_components,
    indices_of_nearest_neighbors_from_distances,
)

EMBEDDING_MODEL = "text-embedding-3-small"
dataset_path = "actions/Recommender_Embeddings/data/Products_Catalog-002.csv"
embedding_cache_path = "actions/Recommender_Embeddings/data/recommendations_embeddings_cache.pkl"
embedding_cache = {}
df_strings_to_embed = pd.DataFrame()
product_descriptions = pd.DataFrame()
df = pd.DataFrame()

def initialize_product_embeddings():

    global df

    # load data 
    df = pd.read_csv(dataset_path)

    n_examples = 3
    df.head(n_examples)

    # Extract a column from the first DataFrame
    # better fix is filtered/hybrid search using Vector DB

    extracted_col = df["Gender"]
    
    # Add the extracted column to the second DataFrame
    df2 = pd.concat([df, extracted_col.rename("Gender")], axis=1)

    df2.head()

    # ### Build cache to save embeddings
    # 
    # The cache is a dictionary that maps tuples of `(text, model)` to an embedding, which is a list of floats. The cache is saved as a Python pickle file.

    df_strings_to_embed['ConcatenatedValues'] = df2.apply(lambda c: f'{c.name} = '+c).agg(' | '.join, axis=1)

    df_strings_to_embed.head()

   
    # load the cache if it exists, and save a copy to disk
    try:
        embedding_cache = pd.read_pickle(embedding_cache_path)
    except FileNotFoundError:
        embedding_cache = {}
    with open(embedding_cache_path, "wb") as embedding_cache_file:
        pickle.dump(embedding_cache, embedding_cache_file)



# define a function to retrieve embeddings from the cache if present, and otherwise request via the API
def embedding_from_string(
    string: str,
    model: str = EMBEDDING_MODEL,
    embedding_cache=embedding_cache
) -> list:
    """Return embedding of given string, using a cache to avoid recomputing."""
    if (string, model) not in embedding_cache.keys():
        embedding_cache[(string, model)] = get_embedding(string, model)
        with open(embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(embedding_cache, embedding_cache_file)
    return embedding_cache[(string, model)]




# ### Recommend similar products based on embeddings
# 
# To find similar products, let's follow a three-step plan:
# 1. Get the similarity embeddings of all the product descriptions
# 2. Calculate the distance between the query  and the products
# 3. Print out the products closest to the query



def print_recommendations_from_strings(
    query_products: str,
    k_nearest_neighbors: int = 1,
) -> list[int]:
    
    global product_descriptions
    initialize_product_embeddings()

    model=EMBEDDING_MODEL
    """Print out the k nearest neighbors of a given string."""
    product_descriptions = df_strings_to_embed["ConcatenatedValues"].tolist()

    # get embeddings for all strings
    embeddings = [embedding_from_string(string, model=model) for string in product_descriptions]
    
    query_products_embedding = get_embedding(query_products, EMBEDDING_MODEL)

    
    # get distances between the query_products_embedding and product embeddings (function from utils.embeddings_utils.py)
    distances = distances_from_embeddings(query_products_embedding, embeddings, distance_metric="cosine")
    
    # get indices of nearest neighbors (function from utils.utils.embeddings_utils.py)
    indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)

    
    # print out its k nearest neighbors
    k_counter = 0
    for i in indices_of_nearest_neighbors:
        # stop after printing out k products
        if k_counter >= k_nearest_neighbors:
            break
        k_counter += 1

        # print out the similar strings and their distances
        print(
            f"""
        --- Recommendation #{k_counter} (nearest neighbor {k_counter} of {k_nearest_neighbors}) ---
        String: {product_descriptions[i]}
        Distance: {distances[i]:0.3f}"""
        )
    
    return indices_of_nearest_neighbors


   




