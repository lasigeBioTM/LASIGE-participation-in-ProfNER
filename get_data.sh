
# Download ProfNER corpus
wget https://zenodo.org/record/4563995/files/profner.zip?download=1
unzip profner.zip?download=1

# Download occupations gazeteer
wget https://zenodo.org/record/4524659/files/occupations-gazetteer.zip?download=1
unzip occupations-gazetteer.zip?download=1

# Download FastText Spanish Twitter embeddings
mkdir embeddings
cd embeddings
wget https://zenodo.org/record/4449930/files/cbow_uncased.tar.gz?download=1
unzip cbow_uncased.tar.gz?download=1
cd ..
