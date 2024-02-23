import numpy as np
import umap
import openai
import matplotlib.pyplot as plt
import mplcursors

# Set your OpenAI API key
openai.api_key = 'your-api-key'

# Assuming 'descriptions' is a list of unit descriptions
descriptions = ["description1", "description2", ...]
unit_names = ["unit1", "unit2", ...]  # Assuming 'unit_names' is a list of corresponding unit names
class_labels = ["class1", "class2", ...]  # Assuming 'class_labels' is a list of class labels for each unit

# Use OpenAI API for text generation
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt="\n".join(descriptions),
    max_tokens=150  # Adjust based on your needs
)

# Extract vectorized results from OpenAI response
vectorized_results = response['choices'][0]['text']
vectorized_results = vectorized_results.split("\n")  # Assuming the OpenAI API response provides vectorized text on separate lines

# Convert the vectorized results into a numerical format (e.g., embedding vectors)
embedding_vectors = []  # Replace this with your actual conversion logic
for result in vectorized_results:
    # Convert each line of vectorized text into a numerical format
    # Modify this part based on your specific data and conversion needs
    vector = np.fromstring(result, sep=' ')
    embedding_vectors.append(vector)

# Convert the list of embedding vectors to a NumPy array
embedding = np.array(embedding_vectors)

# Group units by class
class_data = {}
for i, class_label in enumerate(class_labels):
    if class_label not in class_data:
        class_data[class_label] = []
    class_data[class_label].append((unit_names[i], embedding[i]))

# Plot each class with a shaded circle and a title
fig, ax = plt.subplots()
circles = {}
for class_label, unit_data in class_data.items():
    sc = ax.scatter(*zip(*[coord for _, coord in unit_data]), label=class_label, alpha=0)
    
    # Calculate the center and radius for the circle
    center = np.mean([coord for _, coord in unit_data], axis=0)
    radius = np.max(np.linalg.norm(np.array([coord for _, coord in unit_data]) - center, axis=1))
    
    # Plot the shaded circle
    circle = plt.Circle(center, radius, color='gray', alpha=0.2)
    ax.add_patch(circle)
    
    # Annotate the circle with the class title
    plt.annotate(class_label, center, ha='center', va='center', size=12, weight='bold', color='black')
    
    circles[sc] = {'class_label': class_label, 'unit_data': unit_data}

# Add interactivity to display unit names on click
mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(", ".join([unit for unit, _ in circles[sel.artist]['unit_data']])))
plt.title('Interactive UMAP of Units based on OpenAI Embeddings')
plt.legend()

plt.show()
