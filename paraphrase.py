# from parrot import Parrot
from cmath import e
import torch
import warnings
warnings.filterwarnings("ignore")
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize

# def find_syno(word):
#     synonyms = []
#     for syn in wordnet.synsets(word, lang='fra'):
# 	    for l in syn.lemmas('fra'):
# 		    synonyms.append(l.name())
#     return(synonyms)

# def syno_sentences(sentence):
#     d=[]
#     words = pos_tag(word_tokenize(sentence))
#     i=0
#     for word in words : 
#         if word[1]!= 'DT':
#             i+i+1
#             d.append([word])
#             for syno in find_syno(word):
#                 if syno not in d[i-1]:
                    d[i-1].append(syno)
    print(d)
    # l=d[0]
    # for i in range (len(d)):
    #     if len(d[i])>len(l):
    #         l=d[i]
    # return(l)




    

# print(syno_sentences("quel est ton tableau préféré"))


# # uncomment to get reproducable paraphrase generations
def random_state(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    return(torch.cuda.manual_seed_all(seed))
print(random_state(1234))


# Init models (make sure you init ONLY once if you integrate this to your code)
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)

phrases = [" How do you feel ? ",
    " I'm fine and you ?",
    " how are you ?",
    " Are you feeling anything ?",
    " What do you feel ?",
    " How was your day ?",
]

for phrase in phrases:
  print("-"*100)
  print("Input_phrase: ", phrase)
  print("-"*100)
  print("-"+phrase)
  para_phrases = parrot.augment(input_phrase=phrase)
  for para_phrase in para_phrases:
    
   print("- "+ para_phrase[0])