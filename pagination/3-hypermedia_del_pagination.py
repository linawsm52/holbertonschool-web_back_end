#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination module.
"""
import csv
import math
from typing import List, Dict, Any


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Reads and caches the dataset from the CSV file.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Dataset indexed by sorting position, starting at 0.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Return a dictionary with pagination metadata resilient to deletion.
        """
        assert isinstance(index, int) and index >= 0
        assert isinstance(page_size, int) and page_size > 0

        indexed_data = self.indexed_dataset()
        data_len = len(indexed_data)
        
        assert index < data_len

        data = []
        current_index = index
        count = 0
        
        while count < page_size and current_index < data_len:
            item = indexed_data.get(current_index)
            if item:
                data.append(item)
                count += 1
            current_index += 1

        next_index = current_index if current_index < data_len else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }
