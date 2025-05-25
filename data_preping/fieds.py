WOS_FIELDS = {
    'PT': 'Document Type',
    'AU': 'Authors',
    'TI': 'Title',
    'SO': 'Source',
    'LA': 'Language',
    'DE': 'Keywords',
    'AB': 'Abstract',
    'C1': 'Author Address',
    'RP': 'Repring Adress',
    'CR': 'Cited References',
    'TC': 'Times Cited',
    'PY': 'Publication Year',
    'DI': 'Digital Object Identifier (DOI)',
}

CROSSREF_AVAILABLE_FIELDS = {
    'Title': 'title',
    'Language': 'language',
    'Cited References': 'reference',
    'Times Cited': 'is-referenced-by-count',
    'Publication Year': 'created',
    'Digital Object Identifier (DOI)': 'DOI'
}

REFERENCE_FIELDS = ["article-title", "author", "year", "key"]