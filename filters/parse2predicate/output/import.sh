for i in {0..549}
do
    mongoimport -d law_db -c semantic_sent_temp  semanticSent$i.json; 
done
