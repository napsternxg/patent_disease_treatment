#!/usr/bin/env python
from __future__ import print_function
import csv
import nltk
import re

GRANTID=0
TITLE=1
ABSTRACT=2
_DIGITS = re.compile('\d')
_SPCHARS = re.compile('[\)\-;\(\']')

INDEX_DIR = {"WORD": 0,"PREV_WORD": 1, "NEXT_WORD": 2, "IN_TITLE_ABS": 3, "IS_CAP": 4, "HAS_NUM":5 ,"HAS_SPCHAR": 6, "POS": 7, "CHUNK": 8, "IS_COMP": 9, "IS_MESH": 10, "LABEL": 11}
VAL_DIR = {
    "IN_TITLE_ABS": ["IN_TITLE","IN_ABS"],
    "IS_CAP": ["NO_CAP","IS_CAP", "ALL_CAPS"],
    "HAS_NUM": ["NO_NUM","HAS_COMP", "ALL_NUMS"],
    "HAS_SPCHAR": ["NO_SPCHAR","HAS_SPCHAR"],
    "IS_COMP": ["NO_COMP","IS_COMP"],
    "IS_MESH": ["NO_MESH", "IS_MESH"]
    }
"""
Word Vector:
  <WORD> <PREV_WORD> <NEXT_WORD> IN_TITLE|IN_ABSTRACT CAP|NOCAP HASNUM|HASNONUM HAS_SPECIALCHAR|NO_SPECIALCHAR POS CHUNK IS_COMPOUND IS_MESH <LABEL:DRUG|DISEASE|TYPE|OTHER> 

  PREV_WORD and NEXT_WORD = _ for padding cases. 
"""

def inTitle(i):
  IN_TITLE = VAL_DIR["IN_TITLE_ABS"][0]
  IN_ABS = VAL_DIR["IN_TITLE_ABS"][1]
  return IN_TITLE if i == 1 else IN_ABS

def isCap(word):
  CAP = VAL_DIR["IS_CAP"][1]
  NOCAP = VAL_DIR["IS_CAP"][0]
  ALLCAPS = VAL_DIR["IS_CAP"][2]
  if word.isupper():
    return ALLCAPS
  if len(word) < 1:
    return NOCAP
  return CAP if word[0].isupper() else NOCAP

def hasNum(word):
  HAS_NUM = VAL_DIR["HAS_NUM"][1]
  HAS_NONUM = VAL_DIR["HAS_NUM"][0]
  ALL_NUM = VAL_DIR["HAS_NUM"][2]
  try:
    float(word)
    return ALL_NUM
  except ValueError:
    if len(word) < 1:
      return HAS_NONUM
    return HAS_NUM if _DIGITS.search(word[0]) else HAS_NONUM
  return HAS_NONUM

def hasSPChar(word):
  HAS_SPC = VAL_DIR["HAS_SPCHAR"][1]
  HAS_NOSPC = VAL_DIR["HAS_SPCHAR"][0]
  if len(word) < 1:
    return HAS_NOSPC
  if '.' in word:
    if word[-1] == '.':
      return HAS_NOSPC
    else:
      return HAS_SPC
  return HAS_SPC if _SPCHARS.search(word[0]) else HAS_NOSPC

def prev_next_words(tokens, i):
  prev_word = "_"
  next_word = "_"
  stop_chars = ['.','?',';']
  if i != 0 and tokens[i-1][0] not in stop_chars:
    prev_word = tokens[i-1]
  if tokens[i][-1] not in stop_chars and i < len(tokens)-1:
    next_word = tokens[i+1]
    if next_word[-1] in stop_chars:
      next_word = next_word[:-1]
  return [prev_word, next_word] 


def isCompound(tokens):
  IS_COMP = VAL_DIR["IS_COMP"][1]
  NO_COMP = VAL_DIR["IS_COMP"][0]
  comp_tags = [NO_COMP]*len(tokens)
  for i in range(len(tokens)):
    if 'acid' in tokens[i].lower():
      comp_tags[i] = IS_COMP
      comp_tags[i-1] = IS_COMP
    if 'derivative' in tokens[i].lower():
      comp_tags[i] = IS_COMP
      comp_tags[i-1] = IS_COMP
    if re.search("[\-'{},\[\]\(\)0-9]{2,}[A-Za-z]*", tokens[i]):
      comp_tags[i] = IS_COMP
  return comp_tags

MESH_REGEX = ""
with open("NervousDiseases_clean.txt") as fp:
  lines = fp.read().splitlines()
  MESH_REGEX = "|".join(lines)
MESH_REGEX = "(^|[\s\.\?;]+)("+MESH_REGEX+")($|[\s\.\?;])"
MESH_REGEX = re.compile(MESH_REGEX, re.IGNORECASE)

def isMesh(tokens):
  global MESH_REGEX
  IS_MESH = VAL_DIR["IS_MESH"][1]
  NO_MESH = VAL_DIR["IS_MESH"][0]
  mesh_tags = [NO_MESH]*len(tokens)
  line = " ".join(tokens)
  len_toks = []
  for i in range(len(tokens)):
    len_toks.append(sum([len(x)+1 for x in tokens[:i]]))
  #print(len_toks)
  for m in MESH_REGEX.finditer(line):
    #print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
    #print('%02d-%02d: %s' % (m.start(2), m.end(2), m.group(2)))
    try:
      m_start = len_toks.index(m.start(2))
    except ValueError:
      m_start = max([i for i in range(len(len_toks)) if len_toks[i] < m.start(2)])
    while m_start < len(len_toks) and len_toks[m_start] < m.end(2):
      #print("M_start: ", m_start)
      mesh_tags[m_start] = IS_MESH
      m_start += 1
  return mesh_tags

def getLable(item):
  global INDEX_DIR
  if item[INDEX_DIR["IS_COMP"]] == VAL_DIR["IS_COMP"][1]:
    if item[INDEX_DIR["IS_MESH"]] == VAL_DIR["IS_MESH"][1]:
      return "DISEASE"
    return "TREATEMENT"
  if item[INDEX_DIR["IS_MESH"]] == VAL_DIR["IS_MESH"][1]:
    return "DISEASE"
  return "OTHER"


  
#all_words = []
SPLIT_REGEX = re.compile('; |, | |\.|\?')
with open("matched_patents_final_xl_edit.txt") as fp:
  reader = csv.reader(fp, delimiter="\t")
  stop_chars = ['.','?',';']
  for line in reader:
    print(line)
    all_words = []
    for i in [TITLE,ABSTRACT]:
      #tokens = SPLIT_REGEX.split(line[i])
      tokens = line[i].split()
      tagged = nltk.pos_tag(tokens)
      entities = nltk.chunk.ne_chunk(tagged)
      chunk_tags = nltk.chunk.util.tree2conlltags(entities)
      comp_tags = isCompound(tokens)
      mesh_tags = isMesh(tokens)
      for j in range(len(tokens)):
        item = []
        """
        Word
        """
        item.append(tokens[j])
        if item[0][-1] in stop_chars:
          item[0] = item[0][:-1]
        """
        Previous/Next Word
        """
        item += prev_next_words(tokens, j)
        """
        IN_TITLE/IN_ABSTRACT
        """
        item.append(inTitle(i))
        """
        CAP/NOCAP
        """
        item.append(isCap(tokens[j]))
        """
        HASNUM|HASNONUM
        """
        item.append(hasNum(tokens[j]))
        """
        HAS_SPECIALCHAR|NO_SPECIALCHAR
        """
        item.append(hasSPChar(tokens[j]))
        """
        POS
        """
        item.append(tagged[j][1])
        """
        CHUNK
        """
        item.append(chunk_tags[j][2])
        """
        COMPOUND WORD
        """
        item.append(comp_tags[j])
        """
        MESH WORD
        """
        item.append(mesh_tags[j])
        """
        GET LABEL
        """
        label = getLable(item)
        item.append(label)


        all_words.append(item)
      with open("train_data/{0}.txt".format(line[0]), 'wb+') as fp1:
        for word in all_words:
          print(' '.join([str(k) for k in word]), file=fp1)
    #break
#print(all_words)
