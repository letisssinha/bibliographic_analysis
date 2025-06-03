##repeated


FREQUENCY_FIELDS = {
    'AU': 'Authors',
    'DE': 'Keywords',  ## get for each keyword insead of the line
    'CR': 'Cited References', ## this is not very accurate but ok, also need to check for each reference..
    'PY': 'Publication Year', ## no need to count this (or does it?)
    'TI': 'Title',
    'TI': 'Abstract'
}

COLUMN_NAMES = ["citation_index", "item_index", "citation_item"]
ITEMS_COLUMN = COLUMN_NAMES[2]
INDEX_COLUMN = COLUMN_NAMES[0]
COUNT_COLUMN = "item_count"
CUMULATIVE = 'cumulative'
NUMBER_OF_ITEMS = 'num_items'
FREQUENCY_COLUMN = 'frequency'

FILES_FIELDS = {
    'TI': 'Title',
    'AB': 'Abstract',
    'AB2': 'Abstract Keywords',
    'C1': 'Author Address',
    'AU': 'Authors',
    'DE': 'Keywords',
    'CR': 'Cited References',
    'TC': 'Times Cited',
    'PY': 'Publication Year',
}