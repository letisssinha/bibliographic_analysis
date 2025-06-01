##repeated


FREQUENCY_FIELDS = {
    'AU': 'Authors',
    'DE': 'Keywords',  ## get for each keyword insead of the line
   ## 'AB': 'Abstract',  ## get words that frequently appear and out of the common words
    'CR': 'Cited References', ## this is not very accurate but ok, also need to check for each reference..
   ## 'TC': 'Times Cited',
    'PY': 'Publication Year', ## no need to count this (or does it?)
    'TI': 'Title'
}

COLUMN_NAMES = ["citation_index", "item_index", "citation_item"]
ITEMS_COLUMN = COLUMN_NAMES[2]
INDEX_COLUMN = COLUMN_NAMES[0]
COUNT_COLUMN = "item_count"
CUMULATIVE = 'cumulative'
NUMBER_OF_ITEMS = 'num_items'
FREQUENCY_COLUMN = 'frequency'