#%%
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

#%%
def apriori_model(dataset, min_support=0.3, min_confidence=0.6):
    te = TransactionEncoder()
    te_array = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_array, columns=te.columns_)

    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

    return rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]

# %%
