import os
import re
import nltk

# Ensure stopwords are available in NLTK
try:
    from nltk.corpus import stopwords
except LookupError:
    nltk.download('stopwords')
    from nltk.corpus import stopwords

# Initialize stopwords set and define regex patterns
stopword_set = set(stopwords.words("english"))
punctuation_pat = re.compile(r"""([!"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~])""")
multiwhite_pat = re.compile(r"\s+")
cid_pat = re.compile(r"\(cid:\d+\)")

# Define a function to clean text for readability
def clean_text(txt):
    txt = txt.lower()
    txt = cid_pat.sub(" UNK ", txt)
    txt = punctuation_pat.sub(r" \1 ", txt)
    txt = re.sub("\n+", " ", txt)  # Replace newlines with a single space
    txt = multiwhite_pat.sub(" ", txt).strip()  # Normalize spaces
    return " ".join(["START", txt, "END"])

# Preprocess function to create segmented output with enhanced readability
def preprocess_bbc_dataset(dataset_folder, output_path):
    segmented_text = []
    for category in ['business', 'entertainment', 'politics', 'sport', 'tech']:
        category_path = os.path.join(dataset_folder, category)
        files = os.listdir(category_path)
        
        for file in files:
            file_path = os.path.join(category_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                article = f.read().strip()
                # Clean the text with updated readability focus
                article = clean_text(article)
                segmented_text.append(article)
                segmented_text.append("===END===")  # Article boundary marker

    # Save cleaned, segmented text
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("\n\n".join(segmented_text))

# Paths for dataset and output
dataset_folder = r'C:\Users\PC\Downloads\BBC DATASET\bbc'
output_path = r'C:\Users\PC\Downloads\BBC_DATASET_segmented_final.txt'
preprocess_bbc_dataset(dataset_folder, output_path)

print(f"Processing complete. Saved at '{output_path}'")
