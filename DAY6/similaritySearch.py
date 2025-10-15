from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


paragraphs = [
    "Artificial Intelligence is transforming industries through automation and data analysis.",
    "Machine learning, a subset of AI, enables computers to learn patterns from data and make predictions.",
    "Deep learning is a powerful technique using neural networks to process complex data such as images and speech.",
    "Data science combines statistics, machine learning, and domain expertise to extract insights from data.",
    "Natural Language Processing helps computers understand and generate human language.",
    "Computer vision allows systems to interpret and understand the visual world from images and videos.",
    "AI applications include chatbots, recommendation systems, autonomous vehicles, and fraud detection.",
    "Renewable energy sources such as solar and wind are critical for sustainable development.",
    "Climate change impacts ecosystems and economies around the world, requiring global cooperation.",
    "Energy efficiency technologies can help reduce carbon emissions and fight climate change."
]


vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(paragraphs)

cosine_sim_matrix = cosine_similarity(X)

df = pd.DataFrame(cosine_sim_matrix, 
                  index=[f"P{i+1}" for i in range(len(paragraphs))], 
                  columns=[f"P{i+1}" for i in range(len(paragraphs))])

print("Cosine Similarity Matrix:\n")
print(df.round(2))


np.fill_diagonal(cosine_sim_matrix, 0)
most_similar = np.unravel_index(np.argmax(cosine_sim_matrix), cosine_sim_matrix.shape)
print("\nMost similar paragraphs:")
print(f"Paragraph {most_similar[0]+1} and Paragraph {most_similar[1]+1}")
print("\nP1:", paragraphs[most_similar[0]])
print("\nP2:", paragraphs[most_similar[1]])
