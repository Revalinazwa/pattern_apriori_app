#%%
DATASET = []

def get_dataset():
    return DATASET

def add_transaction(transaction):
    DATASET.append(transaction)

def update_transaction(index, new_transaction):
    if 0 <= index < len(DATASET):
        DATASET[index] = new_transaction
        return True
    return False

def delete_transaction(index):
    if 0 <= index < len(DATASET):
        del DATASET[index]
        return True
    return False

# %%
