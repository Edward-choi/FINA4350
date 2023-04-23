# Data training

In this blog post, we will discuss how we use BERT to conduct sentiment analysis to the textual we collected before.

## BERT

BERT (Bidirectional Encoder Representations from Transformers) is a pre-trained natural language processing (NLP) model developed by Google. It is based on the Transformer architecture, which is a neural network architecture designed to handle sequential data, such as natural language.

BERT is pre-trained on a large corpus of text data and can be fine-tuned on specific NLP tasks, such as sentiment analysis, question-answering, and text classification. It has achieved state-of-the-art results on many NLP benchmarks and has become a popular choice for NLP tasks.

For sentiment analysis, BERT can be fine-tuned on a dataset of labeled text, where each text sample is labeled with a sentiment score (e.g. positive, negative, neutral). The fine-tuning process involves adjusting the pre-trained weights of BERT to optimize the model for the specific sentiment analysis task.

During inference, BERT takes in a sentence or a piece of text, and encodes it into a fixed-dimensional vector representation. This representation can be fed into a classifier (e.g. a neural network) that predicts the sentiment of the input text.

In this project, we will use BERT to analyse Jim Cramer's attitude towards each stocks he mentioned, rating them on a scale from 1 (most negative) to 5 (most positive).

### Fine-tuning