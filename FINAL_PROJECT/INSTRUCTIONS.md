# Instructions for the Naruto Search Engine

Hello and welcome to **HALM Naruto Search**! 

Halm Naruto search works on the Dataset of English subtitles to 200+ episodes of the Japanese anime series Naruto ( https://en.wikipedia.org/wiki/Naruto )

To get the **Naruto Search Engine** to work you need to download the **FINAL_PROJECT** folder with all of its contents (except the Tests folder is not necessary), and run it via Flask python framework.

## Search modes

There are 3 different search modes – **Boolean**, **TF-IDF** and **Stems**. Before inputting the keyword you want to find you have to choose one of the 3 search modes!

### Boolean Search
Boolean search allows to look for a single term (e.g. "cat"), or also for a combinations of terms joined by Boolean operators **AND**, **NOT**, **OR NOT** (e.g. "cat OR dog"). Boolean operators in the input-field should be CAPITALISED so that search engine understands them as logical operators and not as the words to look for.
Boolean search outputs relevant documents in the order of their appearance in the dataset. The output shows the episode number, the sentence in which the term appears on and the exact time code for it.

### TF-IDF Search
TF-IDF search evaluates documents by significance related to the search term and sorts the output starting with the most significant documents. The most significant (= best match) results are calculated using TfidfVectorizer from sklearn library.
TF-IDF search has the added functionality that it can look for bigrams. To search for bigrams, user has to wrap the string in double quotes (" "), e.g. "good cats" will look for exactly this bigram, but not for separate "good" or "cats" in the dataset. The output shows the number of the episode and the number of hits inside that episode in a descending order from the highest significance to the lowest.


### Stems search
Stems search mode allows to find different forms of the search word. To process data for Stem search we use PorterStemmer() from nltk library. As with the boolean search the output given is the number of the episode and the sentence where the term appears as well as the exact time code.
 
## Visualizations
 
There are 3 kinds of visualizations (plots) made for the Naruto dataset. As these plots deal with appearances of heroes on timeline and other static data – visualizations are plotted in a separate plots.html file, so that they do not clutter the main Search view.

### Wordclouds
The are 2 Wordcloud visualizations – (1) of all HEROES in Naruto series,  (2) of all OTHER words in series – MINUS heroes names and stopwords.    

### Scatterplots
There are 2 Scatterplots – (1) of all 89 heroes on timeline, in order of appearance in 219 series, (2) Scatterplot of Heroes who appear in MORE THAN 20 series, ordered by most frequent Heroes.
     
### Horizontal barplot
A Horizontal barplot of Heroes TOTAL mentions and UNIQUE SERIES where this hero is present.
