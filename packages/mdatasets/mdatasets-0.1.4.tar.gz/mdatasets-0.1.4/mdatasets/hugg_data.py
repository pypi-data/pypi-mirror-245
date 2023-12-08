from datasets import load_dataset

def huggingface_dataset(dataset_name, split='train'):
    """
    Load a dataset from the Hugging Face datasets library.

    Parameters:
    - dataset_name (str): The name of the dataset to load (e.g., 'mnist', 'coco', etc.).
    - split (str): The split of the dataset to load (e.g., 'train', 'test', 'validation').

    Returns:
    - dataset: The loaded dataset.

    Example:
    >>> mnist_train = huggingface_dataset('mnist', split='train')
    """

    dataset = load_dataset(dataset_name, split=split)
    return dataset
