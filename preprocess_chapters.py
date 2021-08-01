from collections import defaultdict
from enum import Enum


class DocumentSegmentation(str, Enum):
    book = "book"
    chapter = "chapter"
    sentence = "sentence"


def make_docs(document_segmentation: DocumentSegmentation, min_df, max_df):
    import pandas as pd
    import numpy as np
    import torch
    from sklearn.feature_extraction.text import CountVectorizer
    from glob import glob
    from tqdm import tqdm
    import os

    if document_segmentation == "book":
        books = defaultdict(lambda: "")
        for chapter in tqdm(glob("./bible/*.txt")):
            with open(chapter, "r") as f:
                book_name = os.path.basename(chapter).split("_")[0]
                books[book_name] = books[book_name] + " " + f.read()
        docs = list(books.values())
    elif document_segmentation == "chapter":
        chapters = []
        for chapter in tqdm(glob("./bible/*.txt")):
            with open(chapter, "r") as f:
                chapters.append(f.read())
        docs = chapters
    elif document_segmentation == "sentence":
        sentences = []
        for chapter in tqdm(glob("./bible/*.txt")):
            with open(chapter, "r") as f:
                sentences.extend(f.read().replace(";", ".").split("."))
        docs = sentences
    vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, stop_words="english")

    print(f"vectorizing {len(docs)} documents...")
    print(
        f"""example document:
                    {docs[0]}
    """
    )
    docs = torch.from_numpy(vectorizer.fit_transform(docs).toarray())

    vocab = pd.DataFrame(columns=["word", "index"])
    vocab["word"] = vectorizer.get_feature_names()
    vocab["index"] = vocab.index

    print(
        "Dictionary size: %d" % len(vocab)
    )  # 12722 for 20 newsgroups but only 1678 for the Bible chapters
    print(
        "Corpus size: {}".format(docs.shape)
    )  # 18846 for 20 newsgroups, but only 1299 for Bible chapters

    return docs, vocab
