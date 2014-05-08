#!/usr/bin/env python
#new_pred.txt act_pred.txt
ACTUAL_FILE="act_pred.txt"
PREDICTED_FILE="out_pred_5000.txt"
def print_conf_mat(conf_mat):
  print "X\t"+("_A\t".join(conf_mat.keys()))
  for k in conf_mat:
    print k+"_P\t",
    for k1 in conf_mat[k]:
      print str(conf_mat[k][k1])+"\t",
    print "\n"


with open(ACTUAL_FILE) as fp1,  open(PREDICTED_FILE) as fp2:
  lines1 = fp1.read().splitlines()
  lines2 = fp2.read().splitlines()
  total = len(lines1)
  conf_mat = {
      "O":{"O":0,"D":0,"T":0},
      "D":{"O":0,"D":0,"T":0},
      "T":{"O":0,"D":0,"T":0}
      }
  matched = 0.
  for i in range(total):
    tag1 = lines1[i].strip()
    tag2 = lines2[i].strip()
    conf_mat[tag1[0]][tag2[0]] += 1
    if tag1 == tag2:
      matched += 1
  print "Matched: ", matched
  print "Total: ", total
  print "Accuracy: ", 100*matched/total
  print_conf_mat(conf_mat)

