from csv import reader
import re
from whoosh.lang.porter import stem
import pickle
import copy
import math


def load_data(filePath = './data/kindle_reviews_medium_sample.csv'):
    with open(filePath, 'r', encoding='utf-8') as read_obj:
        csv_reader = reader(read_obj)
        product_dict = {}
        product_counter = 0
        for row in csv_reader:
            #print(row)
            review_text = row[4]
            #print(review_text)
            review_text = re.sub(r'[&#]*[0-9]*[;]','', review_text)
            review_text = re.sub(r'"', '', review_text)
            review_text = re.sub(r'\'', '', review_text)
            review_text = re.sub(r'[-]+', ' ', review_text)
            review_text = re.sub(r'[\.]+', ' ', review_text)
            review_text = re.sub(r'[\,]+', ' ', review_text)
            review_text = re.sub(r'\&', '', review_text)
            review_text = re.sub(r'[\(\)]', '', review_text)
            review_text = re.sub(r'[\?]+', '', review_text)
            review_text = re.sub(r':', '', review_text)
            #print(review_text)
            if row[1] in product_dict:
                product_dict[row[1]] += ' ' + review_text
            else:
                product_counter += 1
                product_dict[row[1]] = review_text
        return product_dict, product_counter

def clean_data(product_dict):
    for key in product_dict:
        product_dict[key] = re.sub(r'[&#]*[0-9]*[;]','', review_text)

def searchProducts(product_dict, searchKey, products_count):
    results = []

    #get intersection of results
    for token in searchKey.split():
        stemmedSearchKey = stem(token.lower())
        if stemmedSearchKey in product_dict:
            res = product_dict[stemmedSearchKey]
            term_in_products_count = len(res)
            weighted_products = []
            #perform idf
            for product in res.keys():
                weighted_products.append(idfWeighting(term_in_products_count, products_count, res[product], product))
            if results:
                products_to_be_deleted = []
                for overall_product in results:
                    is_product_present = False
                    for recent_product in weighted_products:
                        if overall_product[1]  == recent_product[1]:
                            is_product_present = True
                            break
                    if is_product_present == False:
                        products_to_be_deleted.append(overall_product)
                if products_to_be_deleted:
                    for x in products_to_be_deleted:
                        results.pop(results.index(x))
            else:
                results = copy.deepcopy(weighted_products)

    return results

def idfWeighting(term_in_products_count, products_count, term_in_specific_document_count, productId):
    result = math.log10(products_count/term_in_products_count)*term_in_specific_document_count
    return (result,productId)

def tokenizeText(product_dict):
    product_dict_processed = {}
    for key in product_dict:
        token_counter = 0
        for token in product_dict[key].split():
            token_counter += 1
            stemmedTextToken = stem(token).lower()
            if stemmedTextToken in product_dict_processed:
                if key not in product_dict_processed[stemmedTextToken]:
                    product_dict_processed[stemmedTextToken][key] = 1
                else:
                    product_dict_processed[stemmedTextToken][key] += 1
            else:
                # productId | total occurencies
                product_dict_processed[stemmedTextToken] = {key: 1}
    return product_dict_processed

def saveIndices(product_dict_proccesed):
    with open('./data/indices.txt', 'wb') as f:
        pickle.dump(product_dict_proccesed, f, pickle.HIGHEST_PROTOCOL)

def loadIndices(file_path = './data/indices.txt'):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def beginUserInteraction(product_dict_processed, product_counter):
    inputVal = '';
    while 1:
        inputVal = input('Enter search word or type exit to end program: ')
        if inputVal == 'exit':
            break
        results = searchProducts(product_dict_processed, inputVal, product_counter)
        if len(results) == 0:
            print('Unable to find any results')
        else:
            print(sorted(results, key = lambda x: float(x[0])))
def main():
    product_dict, product_counter = load_data()
    product_dict_processed = tokenizeText(product_dict)
    del product_dict
    saveIndices(product_dict_processed)
    del product_dict_processed
    product_dict_loaded = loadIndices()
    print('here')
    beginUserInteraction(product_dict_loaded,product_counter)
if __name__ == "__main__":
    main()