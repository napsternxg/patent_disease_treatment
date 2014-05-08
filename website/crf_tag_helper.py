from __future__ import print_function
import csv
import sys
import re

def get_list(name):
  ids = []
  with open(name+"_list.txt") as fp:
    ids = fp.read().splitlines()
  return ids

INDEX_DIR = {"WORD": 0,"PREV_WORD": 1, "NEXT_WORD": 2, "IN_TITLE_ABS": 3, "IS_CAP": 4, "HAS_NUM":5 ,"HAS_SPCHAR": 6, "POS": 7, "CHUNK": 8, "IS_COMP": 9, "IS_MESH": 10, "LABEL": 11}
VAL_DIR = {
    "IN_TITLE_ABS": ["IN_TITLE","IN_ABS"],
    "IS_CAP": ["NO_CAP","IS_CAP", "ALL_CAPS"],
    "HAS_NUM": ["NO_NUM","HAS_COMP", "ALL_NUMS"],
    "HAS_SPCHAR": ["NO_SPCHAR","HAS_SPCHAR"],
    "IS_COMP": ["NO_COMP","IS_COMP"],
    "IS_MESH": ["NO_MESH", "IS_MESH"]
    }
def get_data(name,grant_id):
  data = {}
  title = []
  abstract = []
  data["grant_id"] = grant_id
  with open("{0}/{1}.txt".format(name,grant_id)) as fp:
    tokens = fp.read().splitlines()
    for token in tokens:
      tags = token.split()
      if tags[INDEX_DIR['IN_TITLE_ABS']] == VAL_DIR['IN_TITLE_ABS'][0]:
        title.append((tags[INDEX_DIR['WORD']],tags[INDEX_DIR['LABEL']]))
      elif tags[INDEX_DIR['IN_TITLE_ABS']] == VAL_DIR['IN_TITLE_ABS'][1]:
        abstract.append((tags[INDEX_DIR['WORD']],tags[INDEX_DIR['LABEL']]))
  data['title'] = title
  data['abstract'] = abstract
  return data

def put_data(name,grant_id,new_title,new_abstract):
  title = []
  abstract = []
  TITLE_ABS_I = INDEX_DIR['IN_TITLE_ABS']
  TITLE_ABS_V = VAL_DIR['IN_TITLE_ABS']
  LABEL_I = INDEX_DIR['LABEL']
  with open("{0}/{1}.txt".format(name,grant_id)) as fp:
    tokens = fp.read().splitlines()
    for token in tokens:
      tags = token.split()
      if tags[TITLE_ABS_I] == TITLE_ABS_V[0]:
        title.append(tags)
      elif tags[TITLE_ABS_I] == TITLE_ABS_V[1]:
        abstract.append(tags)
  sys.stderr.write("ORIGINAL_TITLE:{0}\n".format(title))
  sys.stderr.write("ORIGINAL_TITLE_LEN:{0}\n".format(len(title)))
  sys.stderr.write("NEW_TITLE_LEN:{0}\n".format(len(new_title)))
  if len(title) != len(new_title):
    raise ValueError
  sys.stderr.write("ORIGINAL_ABSTRACT:{0}\n".format(abstract))
  sys.stderr.write("ORIGINAL_ABSTRACT_LEN:{0}\n".format(len(abstract)))
  sys.stderr.write("NEW_ABSTRACT_LEN:{0}\n".format(len(new_abstract)))
  if len(abstract) != len(new_abstract):
    raise ValueError
  for i in range(len(title)):
    title[i][LABEL_I] = new_title[i]
  for i in range(len(abstract)):
    abstract[i][LABEL_I] = new_abstract[i]
  with open("{0}/{1}.txt".format(name,grant_id), 'wb+') as fp:
    for word in (title+abstract):
      print(' '.join([str(k) for k in word]), file=fp)
   
def get_all_data(name,gids):
  data = []
  for gid in gids:
    data.append(get_data(name,gid))
  return data

def put_all_data(name,gids,title,abstract):
  sys.stderr.write("GIDS:{0}\n".format(gids))
  sys.stderr.write("TITLE:{0}\n".format(title))
  sys.stderr.write("ABSTRACT:{0}\n".format(abstract))
  for gid in gids:
    put_data(name,gid,title[gid],abstract[gid])
    sys.stderr.write("Finished updating GID: {0}".format(gid))

def get_form_list(sKey, f):
  #KEY_REGEX = re.compile(key+r"\[([0-9]+)\]\[([0-9]+)\]")
  KEY_REGEX = re.compile(sKey+r"\[([0-9\[\]]+)\]")
  key_matches = {}
  for key in f.keys():
    value = f[key]
    #print(key,":",value)
    match_exp = KEY_REGEX.search(key)
    if match_exp:
      indexes = match_exp.group(1).split('][')
      if len(indexes) > 2:
        #print("More than 3 levels in array:", sKey)
        continue
      if indexes[0] not in key_matches:
        key_matches[indexes[0]] = {}
      if indexes[1] not in key_matches[indexes[0]]:
        key_matches[indexes[0]][indexes[1]] = value
  return key_matches

def get_list_as_array(kList):
  #print("kList: ", kList)
  temp_list = [""]*len(kList)
  for k in kList:
    temp_list[int(k)] = kList[k]
  return temp_list

if __name__ == "__main__":
  print(get_all_data("shubh"))
