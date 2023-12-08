from datasets import load_dataset

def huggingface_dataset(dataset_name, split='train'):
    dataset = load_dataset(dataset_name, split=split)
    return dataset
