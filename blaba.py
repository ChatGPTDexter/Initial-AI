import numpy as np
import umap
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import mplcursors

# Assuming 'descriptions' is a list of unit descriptions
descriptions = ["description1", "description2", ...]
unit_names = ["unit1", "unit2", ...]  # Assuming 'unit_names' is a list of corresponding unit names
class_labels = ["class1", "class2", ...]  # Assuming 'class_labels' is a list of class labels for each unit

# Step 2: Text Vectorization using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(descriptions)

# Step 3: UMAP Dimensionality Reduction
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='cosine')
embedding = reducer.fit_transform(X.toarray())

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
plt.title('UMAP of Units based on Descriptions')
plt.legend()

plt.show()
