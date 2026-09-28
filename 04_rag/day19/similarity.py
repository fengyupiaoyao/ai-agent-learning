import math


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(x ** 2 for x in b))
    return dot_product / (norm_a * norm_b)


v1 = [1, 2, 3]
v2 = [4, 5, 6]

similarity = cosine_similarity(v1, v2)
print("Cosine Similarity:", similarity)
