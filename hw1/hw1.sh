find ./test_input -name "CS3620*" -print | xargs -I{} bash -c 'FILE={} && echo "beggr" >> $FILE'
