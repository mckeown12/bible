import torch
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud


def plot_word_cloud(b, ax, vocab, n):
    sorted_, indices = torch.sort(b, descending=True)
    df = pd.DataFrame(indices[:100].numpy(), columns=['index'])
    words = pd.merge(df, vocab[['index', 'word']],
                     how='left', on='index')['word'].values.tolist()
    sizes = (sorted_[:100] * 1000).int().numpy().tolist()
    freqs = {words[i]: sizes[i] for i in range(len(words))}
    print(f'word frequencies: {freqs}')
    wc = WordCloud(background_color="white", width=800, height=500)
    wc = wc.generate_from_frequencies(freqs)
    ax.set_title('Topic %d' % (n + 1))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")


def plot_word_clouds(beta, vocab, name):
    from math import sqrt, floor
    num_plots = beta.shape[0]
    a = floor(sqrt(num_plots))
    if a*(a+1) < num_plots:
        b = a+1
    else:
        b = a
    fig, axs = plt.subplots(b, a+1, figsize=(14, 10))

    for n in range(num_plots):
        i, j = divmod(n, a+1)
        plot_word_cloud(beta[n], axs[i, j], vocab, n)
    axs[-1, -1].axis('off')
    plt.savefig(name)