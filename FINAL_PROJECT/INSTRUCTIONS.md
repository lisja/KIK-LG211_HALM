# Instructions for the Naruto Search Engine

Hello and welcome to **HALM Naruto Search**! 

Halm Naruto search works on the Dataset of English subtitles to 200+ episodes of the Japanese anime series Naruto https://en.wikipedia.org/wiki/Naruto.

To get the **Naruto Search Engine** to work you need to download the **FINAL_PROJECT** folder with all of its contents (except the Tests folder is not necessary), and run it via Flask python framework.

## Search modes

There are 3 different search modes – **Boolean**, **TF-IDF** and **Stems**. Before inputting the keyword you want to find you have to choose one of the 3 search modes!

### Boolean Search
Boolean search allows to look for a single term (e.g. "cat"), or also for a combinations of terms joined by Boolean operators **AND**, **NOT**, **OR** (e.g. "cat OR dog"). Boolean operators in the input-field should be CAPITALISED so that search engine understands them as logical operators and not as the words to look for.
Boolean search outputs relevant documents in the order of their appearance in the dataset.

### TF-IDF Search
TF-IDF search evaluates documents by significance related to the search term and sorts the output starting with the most significant documents. The most significant (= best match) results are calculated using TfidfVectorizer from sklearn library.
TF-IDF search has the added functionality that it can look for bigrams. To search for bigrams, user has to wrap the string in double quotes, e.g. "good cats" will look for exactly this bigram, but not for separate "good" or "cats" in the dataset.
that Can search for bigrams when using " "


- Stems
 What are stems
