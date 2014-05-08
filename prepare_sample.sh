ls train_data | sort -R | tail -1000 > sample_list.txt
head -500 sample_list.txt > sneha_list.txt
tail -500 sample_list.txt > shubh_list.txt
mkdir sneha_data
mkdir shubh_data
cat sneha_list.txt | xargs -I {} cp train_data/{} sneha_data/
cat shubh_list.txt | xargs -I {} cp train_data/{} shubh_data/
cat sneha_data/* > sneha_full_data.txt
cut -f 1,12 -d ' ' sneha_full_data.txt > sneha_tag.txt
cat shubh_data/* > shubh_full_data.txt
cut -f 1,12 -d ' ' shubh_full_data.txt > shubh_tag.txt
