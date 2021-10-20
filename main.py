from csv import reader
import re
from whoosh.lang.porter import stem

def load_data(filePath = './data/kindle_reviews_small_sample.csv'):
    with open(filePath, 'r', encoding='utf-8') as read_obj:
        csv_reader = reader(read_obj)
        product_dict = {}
        for row in csv_reader:
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
    results = []
    for token in searchKey.split():
        stemmedSearchKey = stem(token.lower())
        if stemmedSearchKey in product_dict:
            res = product_dict[stemmedSearchKey]
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
    product_dict_processed = {}
    for key in product_dict:
        for token in product_dict[key].split():
            stemmedTextToken = stem(token).lower()
            if stemmedTextToken in product_dict_processed:
                if key not in product_dict_processed[stemmedTextToken]:
                    product_dict_processed[stemmedTextToken].append(key)
            else:
                product_dict_processed[stemmedTextToken] = [key]

    beginUserInteraction(product_dict_processed)
if __name__ == "__main__":
    main()