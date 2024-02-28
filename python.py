from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv
from umap import UMAP
import matplotlib.pyplot as plt
import json

# Load the API key from the .env file

load_dotenv()
api_key = "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"

client = OpenAI(api_key=api_key)    # Initialize the OpenAI client


def get_embeddings_batch(inputs):
    # Call the OpenAI API to get the embeddings for a batch of inputs
    response = client.embeddings.create(
        input=inputs,
        model="text-embedding-3-large"
    )

    # Extract the embeddings
    embeddings = np.array([item.embedding for item in response.data])
    return embeddings

response = input("What class units do you want mapped: ")

# read the text files 
with open(response, 'r') as file: 
    content = file.read()

data = json.loads(content)


# create an array of the unit titles

labels = []
descriptions = []

units = data.get(response, [])


for unit in units:
    labels.append(unit["name"])
    descriptions.append(unit["description"])

embeddings = get_embeddings_batch(descriptions)

# set hyperparameters for umap. try playing around with them
n_neighbors = 4
min_dist = 0.3
n_components = 2
metric = 'cosine'

# Initialize the UMAP model
umap = UMAP(    
    n_neighbors=n_neighbors,
    min_dist=min_dist,
    n_components=n_components,
    metric=metric
)

# Fit the UMAP model to the embeddings
reduced_embeddings = umap.fit_transform(embeddings)

# Plot the reduced embeddings
plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1])
for i, text in enumerate(labels):
    plt.text(reduced_embeddings[i, 0], reduced_embeddings[i, 1], text, fontsize=8)



plt.show()
