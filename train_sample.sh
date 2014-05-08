java -cp "/content/smishra8/nlp/mallet-2.0.7/class:/content/smishra8/nlp/mallet-2.0.7/lib/mallet-deps.jar" cc.mallet.fst.SimpleTagger --train true --model-file disease_drug train_data_all.txt
echo "Done Training"
