"""
============================================================
Topic: Indic Language Stop Words for Natural Language Processing
============================================================
Author Name(s): Khushi Jha
Short Description: This file contains a stop-word list for Marathi,
an Indo-Aryan language written in the Devanagari script. These words
may be used during text preprocessing in Natural Language Processing
(NLP), for example to remove high-frequency function words (pronouns,
postpositions, conjunctions, auxiliary verbs and particles) before
keyword extraction, topic modelling or frequency analysis.
Semester: Monsoon Semester 2026
Affiliation: Department of Humanities and Social Sciences,
Indian Institute of Technology (Indian School of Mines) Dhanbad

Note:
These lists contain illustrative examples only. Please modify them
accordingly.

Marathi is agglutinative: postpositions are often joined to the word
(e.g. "घरात" = "घर" + "-त"). Whole-word matching will therefore not
remove such suffixes; a stemmer or suffix-splitter is needed for that.
============================================================
"""


# 1. Marathi Stop Words
# Language: Marathi
# Script: Devanagari

marathi_stopwords = [
    # Conjunctions and connectives
    "आणि", "व", "किंवा", "पण", "परंतु", "मात्र", "तर", "जर",
    "की", "म्हणून", "कारण", "तसेच", "म्हणजे", "त्यामुळे",

    # Personal pronouns
    "मी", "आम्ही", "आपण", "तू", "तुम्ही", "तो", "ती", "ते",
    "त्या", "स्वतः",

    # Possessives
    "माझा", "माझी", "माझे", "आमचा", "आमची", "आमचे",
    "तुझा", "तुझी", "तुझे", "तुमचा", "तुमची", "तुमचे",
    "आपला", "आपली", "आपले", "त्याचा", "त्याची", "त्याचे",
    "तिचा", "तिची", "तिचे", "त्यांचा", "त्यांची", "त्यांचे",
    "त्यांच्या",

    # Oblique / object pronoun forms
    "मला", "आम्हाला", "तुला", "तुम्हाला", "त्याला", "तिला",
    "त्यांना", "याला", "त्याने", "तिने", "त्यांनी",

    # Demonstratives
    "हा", "ही", "हे", "या", "ह्या", "असा", "अशी", "असे", "अशा",
    "तसा", "तशी", "तसे",

    # Relative and interrogative words
    "जो", "जी", "जे", "ज्या", "ज्याने", "काय", "कोण", "कोणता",
    "कोणती", "कोणते", "कुठे", "कधी", "केव्हा", "कसा", "कशी",
    "कसे", "किती",

    # Quantifiers and determiners
    "सर्व", "सगळे", "सगळी", "काही", "कोणी", "प्रत्येक", "एक",
    "फक्त", "अधिक", "खूप", "अगदी",

    # Postpositions (as separate words)
    "मध्ये", "साठी", "वर", "खाली", "पर्यंत", "पासून", "कडे",
    "कडून", "बरोबर", "सोबत", "नंतर", "आधी", "पूर्वी", "विषयी",
    "बद्दल", "प्रमाणे", "सारखे", "दरम्यान",

    # Adverbs of place and time
    "येथे", "इथे", "तिथे", "तेथे", "आता", "आज", "तेव्हा", "जेव्हा",

    # Auxiliary and copula verb forms
    "आहे", "आहेत", "आहेस", "आहोत", "होता", "होती", "होते",
    "होतो", "असून", "असेल", "असतो", "असते", "असलेल्या",
    "होणार", "झाला", "झाली", "झाले",

    # Light verbs (high-frequency, low content)
    "केला", "केली", "केले", "करून", "करत", "आला", "आली", "आले",
    "गेला", "गेली", "गेले",

    # Negation and particles
    "नाही", "नको", "न", "ना", "च", "सुद्धा", "देखील", "हो",
]

# Remove accidental duplicates while keeping the original order.
marathi_stopwords = list(dict.fromkeys(marathi_stopwords))


def remove_stopwords(text):
    """Return the words of `text` that are not Marathi stop words."""
    return [word for word in text.split() if word not in marathi_stopwords]


if __name__ == "__main__":
    sample = "मी आज शाळेत गेले आणि माझी मैत्रीण पण तिथे होती"
    print("Number of stop words:", len(marathi_stopwords))
    print("Original sentence    :", sample)
    print("After removing stop words:", " ".join(remove_stopwords(sample)))
