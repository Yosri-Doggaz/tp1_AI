import pandas
from numpy import *
import customCross as CCross
import itertools
from mlxtend.frequent_patterns import apriori, association_rules

# Question 1
data = pandas.read_table("market_basket.txt",delimiter="\t",header=0)
# Q 2
print(data.head(10))
# Q 3
print(data.shape)

# Q 4
data.sort_values(by=['ID'])
customCross = CCross.customCross(data)

# Q 5
pandasCross = pandas.crosstab(data.ID,data.Product)
# I developed my own compare function cause the crosstable do not have the same column order
if(CCross.compare(customCross,pandasCross)):
    print("the two crossTable are equal")
else:
    print("the two crossTable are NOT equal check the two output text files customV.txt and PandasV.txt")

# Q 6
print(customCross.iloc[:30,:3])

# Q 7 
MaxProduct = 2
minSup = int(0.025 * customCross.shape[0])
crossFiltred = customCross
counts = data.ID.value_counts()


# calculate the support it 2
productSuport = {}
productSuport[1] = crossFiltred.sum()
productSuport[1] = productSuport[1][productSuport[1] >= minSup]

#generate next and cal sup
def check_product_exist(cross, gener):
    check = 1
    for i in range(gener.__len__()):
        check *= cross[gener[i]]
    return check

keyss= list(productSuport[1].keys())
for items_length in range(2, MaxProduct + 1):
    productSuport[items_length] = {}
    generatedNames = []
    for generated in itertools.combinations(keyss,items_length):
        generatedNames.append(generated)
        sup = crossFiltred[ check_product_exist(crossFiltred,generated) != 0 ].shape[0]
        if(sup >= minSup):
            productSuport[items_length][generated] = sup
        
    productSuport[items_length] = pandas.Series(data=productSuport[items_length],dtype=int64)
    print(productSuport[items_length].head(10))

# Q 7
frq = apriori(data, min_support = 0.025, use_colnames = True)
rules = association_rules(frq, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())
# Q 8
rules[:15]

# Q 9 
def is_inclus(x,rules):
  if len(x)>len(rules):
    return False
  for i in x:
    if not (i in rules) :
      return False
  return True

# Q 10
Rules_itemset=[list(a)+list(c) for a,c in zip(rules['antecedents'],rules['consequents'])]
for i in Rules_itemset:
  if is_inclus(['Aspirin'],i):
    print(i)

# Q 11
for i in Rules_itemset:
  if is_inclus(['Aspirin','Eggs'],i):
    print(i)

# Q 12
rules = association_rules(frq, metric ="confidence", min_threshold = 0.75)

# Q 13
print(rules[:5])

# Q 14
print(rules[rules.lift >= 7])

# Q 15
rules[rules.consequents.str.contains('2pct_Milk', na=False)]


