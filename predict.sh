java -cp "/content/smishra8/nlp/mallet-2.0.7/class:/content/smishra8/nlp/mallet-2.0.7/lib/mallet-deps.jar" cc.mallet.fst.SimpleTagger --model-file disease_drug $1 > $2
echo "Done Testing $1. Output in $2"
