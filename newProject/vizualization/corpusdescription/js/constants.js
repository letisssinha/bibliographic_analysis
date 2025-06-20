export const ITEMS = new Map([
    ['AU', 'Authors'],
    ['DE', 'Keywords'],  // Comment: get for each keyword instead of the line
    ['CR', 'Cited References'],  // Comment: not very accurate but ok, also need to check for each reference..
    ['PY', 'Publication Year'],  // Comment: no need to count this (or does it?)
    ['AB', 'Abstract'],
    ['TI', 'Title']
  ]);

  //tooltips
  export const TOOLTIP_MESSAGES = {
    "#info_fs": "Items from that field will be listed on the left panel in numeric order, based on the number of documents in which they appear.",
    "#info_gt": `Choose between different options:<br/>
      <ul>
        <li>The "Custom" option will display the information in the left panel in a custom representation (either a co-occurrence network, a pie chart, a word cloud or a map)</li>
        <li>The "Distributions" option will produce a histogram of the number of items per publication and a cumulative distribution graph displaying the number of items appearing in at least <i>x</i> documents, for varying <i>x</i>. This last graph uses logarithmic scales on both axes, which is useful to recognize power law relationships, appearing as straight lines.</li>
      </ul>`,
    "#info_sl": "We only display items appearing more than <i>x</i> times, the threshold <i>x</i> being chosen so that the length of the list is less than 10000."
  };

  //files
  export const DATA_DIRECTORY = "data/freqs/";
  export const DISTRIBUTION_FILE = 'DISTRIBS_itemuse.json';
  export const COORELATION_FILE = 'coocnetworks.json'

  //dropdown tab
  export const FIELD_DROPDOWN_ID = 'selectITEM';
  export const GRAPH_DROPDOWN_ID = 'selectGRAPH';
  export const SORT_TAB_ID = '#sortTAB';
  export const SORT_DROPDOWN_ID = 'selectSORTtab';
  export const NONE_AVAILABLE_ID = "#noneAV";
  export const LIST_TAB_ID = "#listTAB";
  export const ITEM_SELECTION_ID = '#itemselection';
  export const GRAPH_SELECTION_ID = '#graphselection';
  export const SORT_OPTIONS = [
    { value: 'NB', text: 'Record count', selected: true },
    { value: 'ITEM', text: 'Item' }
  ];

  //table
  export const TITLE_FONT_SIZE_FOR_R = 0.75;
  export const TITLE_FONT_SIZE_DEFAULT = 0.95;
  export const EPSILON_THRESHOLD = 0.01;
  export const EPSILON_SYMBOL = "&epsilon;";
  export const RECORD_COUNT_HEADER = "Record count";
  export const RECORD_PERCENT_HEADER = "% of ";
  export const RANK_HEADER = "Rank";
  export const ITEM_LABEL_PREFIX = "Item = ";
  export const NO_DATA_NOTE_PREFIX = "<strong>Note: this data is NOT available/existing for ";
  export const NO_DATA_NOTE_SUFFIX = "% of the publications in the studied corpus.</strong>";

  //graph window
  export const HEADER_MENU_ID = '#headermenu';
  export const CONTAINER_ID = '#container';
  export const REDO_CLOUD_ID = '#redocloud';
  export const SLIDER_ID = '#slider';
  export const SIDE_PANEL_ID = '#sidepanel';
  export const GRAPH_ID = '#graph';
  export const WIDTH_OFFSET = 240;
  export const LEFT_BASE = 250;
  export const LEFT_MULTIPLIER = 0.40;
  export const HEIGHT_OFFSET = 50;
  export const HEIGHT_ADJUST = 42;
  export const SLIDER_HEIGHT_OFFSET = 20;
