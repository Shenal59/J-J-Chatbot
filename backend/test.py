import pickle
with open("data/faqs_embeddings.pkl","rb") as f:
    entries, vecs = pickle.load(f)
print(type(entries), type(vecs))