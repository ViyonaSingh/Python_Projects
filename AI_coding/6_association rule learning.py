from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

# Sample dataset: Transactions (you can change these)
transactions = [
    ['milk', 'bread', 'butter'],
    ['milk', 'bread'],
    ['milk', 'cookies'],
    ['bread', 'butter'],
    ['milk', 'bread', 'cookies'],
    ['cookies'],
]

# Step 1: Encode transactions
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)

# Step 2: Ask user for minimum support
min_support = float(input("Enter minimum support (e.g. 0.3): "))
frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)

if frequent_itemsets.empty:
    print(" No frequent itemsets found. Try lowering the support.")
    exit()

# Step 3: Ask user for min confidence, generate rules
min_conf = float(input("Enter minimum confidence (e.g. 0.6): "))
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_conf)

if rules.empty:
    print(" No rules found. Try lowering the confidence.")
    exit()

# Step 4: Show rules
print("\n✅ Association Rules:")
for idx, row in rules.iterrows():
    print(f"RULE {idx+1}: {set(row['antecedents'])} => {set(row['consequents'])}")
    print(f"   support:   {row['support']:.2f}")
    print(f"   confidence:{row['confidence']:.2f}")
    print(f"   lift:      {row['lift']:.2f}")
    print("-" * 40)
