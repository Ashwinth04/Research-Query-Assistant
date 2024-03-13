def all_possible_keywords(query):
    query = query.split(" ")
    l = len(query)
    answers = []
    for stride in range(1,l+1):
        for j in range(0,l-stride+1):
            temp = query[j:j+stride]
            answers.append(" ".join(temp))
    return answers

# print(all_possible_keywords("Tell me in detail about recurrent neural networks"))