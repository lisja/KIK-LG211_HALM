"""from sklearn.feature_extraction.text import CountVectorizer



def count_and_sparse():
    cv = CountVectorizer(lowercase=True, binary=True)
    sparse_matrix = cv.fit_transform(documents)

    print("Term-document matrix: (?)\n")
    print(sparse_matrix)
"""

def search(input_query):
    print("Searching...\n\n")

def interface():
    print("Welcome to HALM search engine!\n")

    while True:
    
        print("'q'= Quit")
        input_query = input("Input your query: ")

        if input_query == "q":
            break
        else:
            search(input_query)
            

def main():
    interface()

main()
    
    
    


