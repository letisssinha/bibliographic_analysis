from collections import Counter
from fields import INDEX_COLUMN, ITEMS_COLUMN
from itertools import combinations
import json



def generate_cooccurrence_network(df_without_duplicates, item_counts, label):
  cooccurrence_pairs = []
  for _, group in df_without_duplicates.groupby(INDEX_COLUMN):
        items = sorted(group[ITEMS_COLUMN])
        cooccurrence_pairs.extend(combinations(items, 2))
  pair_counts = Counter(cooccurrence_pairs)
  item_to_id = {item: idx for idx, item in enumerate(item_counts.index)}
  make_json(item_counts, item_to_id, pair_counts, label)
 
def make_json(item_counts, item_to_id, pair_counts, label):
    nodes = [
        {
            "type": label,
            "name": item_to_id[item],
            "item": item,
            "size": count
        }
        for item, count in item_counts.items()
    ]

    links = [
        {
            "type": label,
            "source": item_to_id[a],
            "target": item_to_id[b],
            "Ncooc": count
        }
        for (a, b), count in pair_counts.items()
    ]

    return {
        "nodes": nodes,
        "links": links
    }






