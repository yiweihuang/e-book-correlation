import gensim

model = gensim.models.Word2Vec.load_word2vec_format("combine_book_slide_model/week1.en.text.vector", binary=False)
# model = gensim.models.Word2Vec.load_word2vec_format("ebook_model/computernetwork.en.text.vector", binary=False)

model.most_similar("queen")

model.most_similar("man")

model.most_similar("woman")

model.similarity("woman", "man")

model.doesnt_match("breakfast cereal dinner lunch".split())

model.similarity("woman", "girl")

model.most_similar("frog")
