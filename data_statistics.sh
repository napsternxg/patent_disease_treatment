# Get total terms in training set
echo "In training set:"
echo "Total DISEASE Terms:"
grep "DISEASE" train_data/* | wc -l
echo "Total TREATEMENT Terms:"
grep "TREATEMENT" train_data/* | wc -l
echo "Total ALL TERMS:"
wc -l train_data/* | tail -1 | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | cut -f 1 -d ' '

# Get total unique terms in training set
echo "Total UNIQUE DISEASE Terms:"
grep -h "DISEASE" train_data/* | cut -f 1 -d ' ' | sort -u | wc -l
echo "Total UNIQUE TREATEMENT Terms:"
grep -h "TREATEMENT" train_data/* | cut -f 1 -d ' ' | sort -u | wc -l

# Get total terms in sample set
echo "In sample set:"
echo "Total DISEASE Terms:"
grep "DISEASE" train_data_all.txt | wc -l
echo "Total TREATEMENT Terms:"
grep "TREATEMENT" train_data_all.txt | wc -l
echo "Total ALL TERMS:"
wc -l train_data_all.txt | tail -1 | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | cut -f 1 -d ' '

# Get total unique terms in sample set
echo "Total UNIQUE DISEASE Terms:"
grep -h "DISEASE" train_data_all.txt | cut -f 1 -d ' ' | sort -u | wc -l
echo "Total UNIQUE TREATEMENT Terms:"
grep -h "TREATEMENT" train_data_all.txt | cut -f 1 -d ' ' | sort -u | wc -l

# Get total terms in test set
echo "In test set:"
echo "Total DISEASE Terms:"
grep "DISEASE" test_set.txt | wc -l
echo "Total TREATEMENT Terms:"
grep "TREATEMENT" test_set.txt | wc -l
echo "Total ALL TERMS:"
wc -l test_set.txt | tail -1 | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | cut -f 1 -d ' '

# Get total unique terms in test set
echo "Total UNIQUE DISEASE Terms:"
grep -h "DISEASE" test_set.txt | cut -f 1 -d ' ' | sort -u | wc -l
echo "Total UNIQUE TREATEMENT Terms:"
grep -h "TREATEMENT" test_set.txt | cut -f 1 -d ' ' | sort -u | wc -l
