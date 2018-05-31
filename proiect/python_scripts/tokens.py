import copy
import json
import os
import sys
import gensim
import nltk


# cuvant_important titlu *0.5
# cuvant_important continut *0.2
# se face un scor care se da mai departe pentru fiecare categorie
def get_raitings(post, model):
    current_dict = {'general': 1, 'technology': 1, 'sports': 1, 'business': 1,
                    'entertainment': 1, 'science': 1}
    result_dict = copy.copy(current_dict)
    for key, value in current_dict.items():
        total_score = 0
        contor = 0
        try:
            for word in post['title'].split(" "):
                token_word = nltk.word_tokenize(word)
                for noun in nltk.pos_tag(token_word):
                    if noun[1] == 'NN':
                        token_key = nltk.pos_tag(key)[0]
                        try:
                            total_score += model.similarity(token_key, noun[0]) * 0.5
                            # print(model.similarity(token_key, noun[0]))
                            contor += 1
                        except KeyError:
                            pass
        except AttributeError:
            pass

        try:
            for word in post['description'].split(" "):
                token_word = nltk.word_tokenize(word)
                for noun in nltk.pos_tag(token_word):
                    if noun[1] == 'NN':
                        token_key = nltk.pos_tag(key)[0]
                        try:
                            total_score += model.similarity(token_key, noun[0]) * 0.2
                            # print(model.similarity(token_key, noun[0]))
                            contor += 1
                        except KeyError:
                            pass
        except AttributeError:
            pass
        try:
            result_dict[key] = total_score[0] + total_score[1]
        except TypeError:
            result_dict[key] = 0.2
            # print(key)
            # print(post['title'])
            # print(total_score)
            # print(contor)
            # print("____")
    return result_dict


def Clasify(folder, model):
    nr_articol = 0
    eval_json_path = os.path.join(os.getcwd(), "evaluations")
    eval_json_path = os.path.join(eval_json_path, folder)

    post_path = os.path.join(os.getcwd(), "posts")
    post_path = os.path.join(post_path, folder)

    for file in os.listdir(post_path):
        file_title = os.path.splitext(file)[0]

        post_json = json.load(open(os.path.join(post_path, file)))

        for key, value in post_json.items():
            if key == "articles":
                for posts in value:  # fiecare post din lista de articole
                    # print(posts)

                    post = json.loads(json.dumps(posts))
                    print(post)


                    try:
                        temp_eval_json_path = os.path.join(eval_json_path,
                                                           post['title'].replace(" ", "_").replace("?", "").replace("!",
                                                                                                                    "")
                                                           .replace("\"", "") + ".json")

                        clasif_dict = get_raitings(post, model)
                        post["clasificare"] = clasif_dict

                        print(post)
                        # temp_eval_json_path = create_normal_json(eval_json_path, file_title)

                        print(temp_eval_json_path)
                        with open(temp_eval_json_path, 'w') as outfile:
                            json.dump(post, outfile)
                    except OSError:
                        continue
                        # temp_post_path = os.path.join(post_path, file)
                        # eval_post(temp_eval_json_path, temp_post_path, model)


def main():
    # ConcatenateSynonyms("file.json")
    print(sys.argv[1])
    # Clasify("general")
    # Clasify("technology")
    # Clasify("sports")
    # Clasify("business")
    # Clasify("entertainment")
    # Clasify("science")


def clasiftAll():
    model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True,
                                                            limit=500000)
    Clasify("general", model)
    Clasify("technology", model)
    Clasify("sports", model)
    Clasify("business", model)
    Clasify("entertainment", model)
    Clasify("science", model)


clasiftAll()
# main()
