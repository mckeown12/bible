#  Code here is based off of the LDA pyro example
#  https://pyro.ai/examples/prodlda.html

from enum import Enum
import typer
from preprocess_chapters import DocumentSegmentation


def main(
    document_segmentation: DocumentSegmentation = DocumentSegmentation.sentence,
    learning_rate: float = 1e-3,
    num_topics: int = 8,
    batch_size: int = 32,
    num_epochs: int = 100,
    max_df: float = 0.5,
    min_df: float = 20,
):
    '''
    Train a ProdLDA model and save a word cloud png summarizing the topics.
    
    `max_df` and `min_df` are passed to `sklearn.feature_extraction.text.CountVectorizer`
    and allow popular or unpopular words to be excluded from the dictionary. All other
    parameters should be straight forward.
    '''

    import torch
    import pyro
    import math
    from pyro.infer import SVI, TraceMeanField_ELBO
    from tqdm import trange
    from models import ProdLDA
    from preprocess_chapters import make_docs
    from wordclouds import plot_word_clouds

    # setting global variables
    seed = 0
    torch.manual_seed(seed)
    pyro.set_rng_seed(seed)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # hack because typer does not support union types :(
    if max_df == int(max_df):
        max_df = int(max_df)
    if min_df == int(min_df):
        min_df = int(min_df)
    docs, vocab = make_docs(document_segmentation, min_df, max_df)
    docs = docs.float().to(device)

    # training
    pyro.clear_param_store()

    prodLDA = ProdLDA(
        vocab_size=docs.shape[1], num_topics=num_topics, hidden=100, dropout=0.2
    )
    prodLDA.to(device)

    optimizer = pyro.optim.Adam({"lr": learning_rate})
    svi = SVI(prodLDA.model, prodLDA.guide, optimizer, loss=TraceMeanField_ELBO())
    num_batches = int(math.ceil(docs.shape[0] / batch_size))

    bar = trange(num_epochs)
    losses = []
    for epoch in bar:
        running_loss = 0.0
        for i in range(num_batches):
            batch_docs = docs[i * batch_size : (i + 1) * batch_size, :]
            loss = svi.step(batch_docs)
            running_loss += loss / batch_docs.size(0)
            losses.append(loss)
        bar.set_postfix(epoch_loss="{:.2e}".format(running_loss))

    # show the word cloud
    plot_name = f"wordcloud_{document_segmentation}_{learning_rate}_{num_topics}_{batch_size}_{num_epochs}_{max_df}_{min_df}.png"
    plot_word_clouds(prodLDA.beta(), vocab, plot_name)


if __name__ == "__main__":
    typer.run(main)
