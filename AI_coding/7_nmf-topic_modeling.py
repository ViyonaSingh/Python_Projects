# this is non-negative matrix factorization
# this code tries to (: find the topic of provided news articles

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import re

# === STEP 1: Sample training news ===
texts = [
    # Politics / Government
    "The prime minister introduced a new climate policy.",
    "Parliament voted to increase education funding.",
    "A controversial immigration bill has been approved.",
    "The government imposed new taxes on imports.",
    "Protests erupted after election results were announced.",

    # Sports
    "The football team celebrated their championship victory.",
    "A new world record was set in the 100m sprint.",
    "The tennis finals drew millions of viewers worldwide.",
    "Basketball teams are preparing for the playoffs.",
    "The Olympic committee revealed the 2028 host city.",

    # Science / Technology
    "Scientists are developing a vaccine for a rare virus.",
    "AI researchers trained a model to diagnose diseases.",
    "A new species of dinosaur was discovered in Argentina.",
    "Tech companies are investing in quantum computing.",
    "NASA is launching a probe to study Jupiter's moons.",

    # Economy / Business
    "Unemployment rates dropped significantly last quarter.",
    "The stock market hit an all-time high this week.",
    "A startup raised $20 million in its funding round.",
    "Inflation concerns affect consumer spending habits.",
    "Banks are tightening lending policies due to risks.",

    # Entertainment / Culture
    "The actor won an award for their performance in a drama.",
    "A new Marvel movie topped the box office charts.",
    "The museum is showcasing modern art from Asia.",
    "Critics praised the latest Broadway musical.",
    "A streaming service released a popular fantasy series.",

    # Environment / Climate
    "Global temperatures hit new highs in July.",
    "Wildfires continue to spread across California.",
    "A new ocean cleanup device was deployed successfully.",
    "Scientists warn about rapid Arctic ice melt.",
    "The UN held a summit on biodiversity conservation.",

    # Health / Lifestyle
    "Doctors are warning about rising diabetes cases.",
    "Studies link sleep quality to brain health.",
    "Yoga and meditation help reduce stress levels.",
    "A new fitness trend is taking over social media.",
    "Experts recommend reducing sugar for heart health.",
]


# === STEP 2: TF-IDF Vectorization ===
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

# === STEP 3: KMeans Clustering ===
num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# === STEP 4: Extract topics for each cluster ===
def get_top_keywords_per_cluster(kmeans_model, vectorizer, n_words=3):
    keywords = []
    centroids = kmeans_model.cluster_centers_
    terms = vectorizer.get_feature_names_out()
    for i in range(num_clusters):
        center = centroids[i]
        top_indices = center.argsort()[-n_words:][::-1]
        top_words = [terms[idx] for idx in top_indices]
        keywords.append(top_words)
    return keywords

cluster_keywords = get_top_keywords_per_cluster(kmeans, vectorizer)

# === STEP 5: Prediction Function ===
def clean(text):
    return re.sub(r'\W+', ' ', text.lower())

def get_most_common_words(text, n=3):
    words = clean(text).split()
    common = Counter(words).most_common(n)
    return [w for w, _ in common]

def predict_topic(text):
    vec = vectorizer.transform([text])
    cluster = kmeans.predict(vec)[0]
    topic_words = cluster_keywords[cluster]

    if not any(word in clean(text) for word in topic_words):
        fallback = get_most_common_words(text, 2)
        return f"⚠️ Weak match. Suggested Topic: {' '.join(fallback).title()}"
    return f"✅ Topic: {' '.join(topic_words).title()}"

# === STEP 6: Interactive Loop ===
print("=== Topic Extractor (type 'exit' to quit) ===")
while True:
    user_text = input("\nEnter your article paragraph:\n")
    if user_text.lower() == 'exit':
        break
    result = predict_topic(user_text)
    print(result)
