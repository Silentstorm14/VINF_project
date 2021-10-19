from csv import reader
import re
from whoosh.analysis import StandardAnalyzer
from whoosh.lang.porter import stem

def load_data(filePath = 'C:/VINF/data/kindle_reviews_small_sample.csv'):
    with open(filePath, 'r', encoding='utf-8') as read_obj:
        csv_reader = reader(read_obj)
        product_dict = {}
        for row in csv_reader:
            if row[1] == 'asin':
                continue
            #print(row)
            review_text = row[4]
            #print(review_text)
            review_text = re.sub(r'[&#]*[0-9]*[;]','', review_text)
            #print(review_text)
            if row[1] in product_dict:
                product_dict[row[1]] += review_text
            else:
                product_dict[row[1]] = review_text
        return product_dict

def clean_data(product_dict):
    for key in product_dict:
        product_dict[key] = re.sub(r'[&#]*[0-9]*[;]','', review_text)

def searchProducts(product_dict, searchKey):
    analyzer = StandardAnalyzer()
    results = []
    for token in analyzer(searchKey):
        stemmedSearchKey = stem(token.text)
        if isinstance(stemmedSearchKey, str):
            if stemmedSearchKey in product_dict:
                res = product_dict[stemmedSearchKey]
                for ttt in res:
                    if ttt not in results:
                        results.append(ttt)
            return results
        for key in stemmedSearchKey:
            if key in product_dict:
                res = product_dict[key]
                for ttt in res:
                    if ttt not in results:
                        results.append(ttt)
        return results
def beginUserInteraction(product_dict_processed):
    inputVal = '';
    while 1:
        inputVal = input('Enter search word or type exit to end program: ')
        if inputVal == 'exit':
            break
        results = searchProducts(product_dict_processed, inputVal)
        if len(results) == 0:
            print('Unable to find any results')
        else:
            print(results)
def main():
    product_dict = load_data()
    analyzer = StandardAnalyzer()
    product_dict_processed = {}
    for key in product_dict:
        for token in analyzer(product_dict[key], removestops=False):
            if token.text == 'Ylesia':
                print('tu')
            stemmedTextToken = stem(token.text)
            if stemmedTextToken in product_dict_processed:
                if key not in product_dict_processed[stemmedTextToken]:
                    product_dict_processed[stemmedTextToken].append(key)
            else:
                product_dict_processed[stemmedTextToken] = [key]
    #print(product_dict_processed['war'])
    #[(print(t.text)) for t in analyzer(u"With Ylesia, a novella originally published in e-book form, Walter Jon Williams gets an opportunity to insert further story into his novel Destiny's Way.", removestops=False)]
    #[print(token.text) for token in stemmer(analyzed_data)]
    #print(product_dict_processed)
    beginUserInteraction(product_dict_processed)
if __name__ == "__main__":
    main()