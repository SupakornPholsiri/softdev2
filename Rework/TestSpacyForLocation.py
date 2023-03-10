import spacy

nlp = spacy.load("th")

text = "บ้านฉันอยู่ที่กรุงเทพมหานคร"

doc = nlp(text)

for ent in doc.ents:
    if ent.label_ == "LOC":
        print(ent.text)
