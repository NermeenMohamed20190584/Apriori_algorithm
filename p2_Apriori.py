from itertools import combinations
import pandas as pd
from collections import Counter

# Load data from Excel file
inputData = pd.read_excel('CoffeeShopTransactions.xlsx')
transactions = pd.DataFrame(inputData, columns=['Item 1', 'Item 2', 'Item 3'])

# data cleaning
transactions = transactions.applymap(lambda x: x.replace( " ", "").lower() if isinstance(x, str) else x)
# store data in list
itemsets = [set(row) for _, row in transactions.iterrows()]

# Define a function to generate frequent itemsets
def generate_frequent_itemsets(itemsets, min_support):

    min_support_count = min_support * len(itemsets)

    
    counter1 = Counter(item for row in itemsets for item in row)

    frequent_items1 = {frozenset([item]): support/len(itemsets) for item, support in counter1.items() if support >= min_support_count}
    
    
    united_items = {i.union(j) for i in frequent_items1 for j in frequent_items1 if i != j and len(i.union(j)) == 2}


    counter2 = {item: sum(1 for row in itemsets if item.issubset(set(row))) for item in united_items}


    frequent_items2 = {item: support/len(itemsets) for item, support in counter2.items() if support >= min_support_count}


    united_items2 = {i.union(j) for i in frequent_items2 for j in frequent_items2 if i != j and len(i.union(j)) == 3}


    counter3 = {itemset: sum(1 for row in itemsets if itemset.issubset(set(row))) for itemset in united_items2}


    frequent_items3 = {item: support/len(itemsets) for item, support in counter3.items() if support >= min_support_count}


    return frequent_items3

# Step 3: Define a function to generate association rules from the frequent itemsets
def generate_association_rules(frequent_items, min_confidence):
  for frequent_item in list(frequent_items):
      combination= [frozenset(q) for q in combinations(frequent_item,len(frequent_item)-1)]

      for first_item in combination:
        third_item = frequent_item-first_item
   
    
        support_of_all_rule = 0
        support_of_first_item = 0
        support_of_third_item = 0

        for iterator in itemsets:
            itemset = set(iterator)
            if(first_item.issubset(itemset)):
                support_of_first_item+=1
            if(third_item.issubset(itemset)):
                support_of_third_item+=1
            if(frequent_item.issubset(itemset)):
                support_of_all_rule+=1
            
        if(support_of_all_rule/support_of_first_item > min_confidence):
          print(str(list(first_item))+" -> "+str(list(third_item))+" = "+str(support_of_all_rule/support_of_first_item))
        if(support_of_all_rule/support_of_third_item > min_confidence):
          print(str(list(third_item))+" -> "+str(list(first_item))+" = "+str(support_of_all_rule/support_of_third_item))


# Step 4: Ask the user for the minimum support and confidence values
min_support = float(input('Enter the minimum support (between 0 : 1) : '))
min_confidence = float(input('Enter the minimum confidence (between 0 : 1) : '))

# Step 5: Use the above functions to generate frequent itemsets and association rules based on the user input and print them

print('\nFrequent Itemsets:\n')

frequent_items = generate_frequent_itemsets(itemsets, min_support)
for itemset, support in frequent_items.items():
    print(f'{set(itemset)}: {support}')

print('\nAssociation Rules:\n')

association_rules = generate_association_rules(frequent_items, min_confidence)