/* ---------------------------------------------------------------------------
   (c) BiblioMaps, 2017
   Author: Sebastian Grauwin
   website: sebastian-grauwin.com
   --------------------------------------------------------------------------- */

/*-------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------------------------------------------------------------*/
import * as CONSTANTS from '/newProject/vizualization/corpusdescription/js/constants.js';
import * as GRAPHS from '/newProject/vizualization/corpusdescription/js/graphs.js';

export function doCDviz(){
  makeGraphWitzWindow()
  d3.json("../" + CONSTANTS.DATA_DIRECTORY + CONSTANTS.DISTRIBUTION_FILE, function(data) {
    const Npapers = data.N;
    var probability_count_value = makeCountValue(data);
    var probability_cumulative_count = makeCumulativeValue(data);
    d3.json("../" + CONSTANTS.DATA_DIRECTORY + CONSTANTS.COORELATION_FILE, function(data) {
      const nodes = data.nodes;
      const links = data.links;
      makeSideBarMenu(Npapers, nodes, links);
    });
  });
}

function makeSideBarMenu(Npapers, nodes, links) {
  const NUM_PUB_ID = '#NUMPUB';
  const selectedField = "AU";

  const GRAPH_OPTIONS = [
    { value: 'custom', text: 'Custom', selected: true },
    { value: 'science', text: 'Distributions', selected: false }
  ];

  const itemOptions = setupItemDropdown(CONSTANTS.ITEMS.keys(), CONSTANTS.ITEMS, selectedField);

  // Pass numPublications to update using closures
  createDropdown(CONSTANTS.ITEM_SELECTION_ID, CONSTANTS.FIELD_DROPDOWN_ID, itemOptions, () => update(Npapers, nodes, links));
  createDropdown(CONSTANTS.GRAPH_SELECTION_ID, CONSTANTS.GRAPH_DROPDOWN_ID, GRAPH_OPTIONS, () => update(Npapers, nodes, links));
  createDropdown(CONSTANTS.SORT_TAB_ID, CONSTANTS.SORT_DROPDOWN_ID, CONSTANTS.SORT_OPTIONS, () => {}); // sort handled later

  d3.select(NUM_PUB_ID).html(Npapers);
  initializeTooltips();
}

function createDropdown(containerSelector, selectId, options, onChangeFn) {
  const container = d3.select(containerSelector).html(''); // clear existing

  const select = container.append('select')
    .attr('id', selectId)
    .style('width', CONSTANTS.SELECT_WIDTH_STYLE)
    .on('change', onChangeFn);

  select.selectAll('option')
    .data(options)
    .enter()
    .append('option')
    .attr('value', d => d.value)
    .property('selected', d => d.selected)
    .text(d => d.text);
}

function setupItemDropdown(fields, items, selectedField) {
  return Array.from(fields).map(f => ({
    value: f,
    text: capitalizeFirstLetter(items.get(f)),
    selected: selectedField === f
  }));
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function makeGraphWitzWindow() {
  const headerMenuWidth = d3.select(CONSTANTS.HEADER_MENU_ID).node().getBoundingClientRect().width;
  const availableWidth = headerMenuWidth - CONSTANTS.WIDTH_OFFSET;

  d3.select(CONSTANTS.CONTAINER_ID).style("width", `${availableWidth}px`);
  d3.select(CONSTANTS.REDO_CLOUD_ID).style("left", `${CONSTANTS.LEFT_BASE + CONSTANTS.LEFT_MULTIPLIER * availableWidth}px`);
  d3.select(CONSTANTS.SLIDER_ID).style("left", `${CONSTANTS.LEFT_BASE + CONSTANTS.LEFT_MULTIPLIER * availableWidth}px`);

  const availableHeight = window.innerHeight - CONSTANTS.HEIGHT_OFFSET;
  const adjustedHeight = availableHeight - CONSTANTS.HEIGHT_ADJUST;
  const sliderTop = availableHeight - CONSTANTS.SLIDER_HEIGHT_OFFSET;

  d3.select(CONSTANTS.CONTAINER_ID).style("height", `${availableHeight}px`);
  d3.select(CONSTANTS.SIDE_PANEL_ID).style("height", `${availableHeight}px`);
  d3.select(CONSTANTS.LIST_TAB_ID).style("height", `${adjustedHeight}px`);
  d3.select(CONSTANTS.GRAPH_ID).style("height", `${adjustedHeight}px`).style("width", "100%");
  d3.select(CONSTANTS.SLIDER_ID).style("top", `${sliderTop}px`);
}

function makeCountValue(data) {
  const probability_count_value = new Map();
  for (const value of CONSTANTS.ITEMS.values()) {
    const countValueFieldName = `${value}_count_value`;
    probability_count_value.set(value, data[countValueFieldName]);
  }
  return probability_count_value;
}

function makeCumulativeValue(data) {
  const probability_cumulative_count = new Map();
  for (const value of CONSTANTS.ITEMS.values()) {
    const cumulativeCountFieldfName = `${value}_cumulative_count`;
    probability_cumulative_count.set(value, data[cumulativeCountFieldfName]);
  }
  return probability_cumulative_count;
}

function initializeTooltips() {
  Object.entries(CONSTANTS.TOOLTIP_MESSAGES).forEach(([selector, message]) => {
    attachTooltip(selector, message);
  });
}

function attachTooltip(targetSelector, tooltipMessage) {
  const TOOLTIP_ID = "#tooltip_bulle";
  const TOOLTIP_CLASS = "tooltip_bulle";
  const TOOLTIP_SHOW_DURATION = 200;
  const TOOLTIP_HIDE_DURATION = 10;
  const TOOLTIP_OFFSET_X = 10;
  const TOOLTIP_OFFSET_Y = 20;

  const tooltip = d3.select(TOOLTIP_ID)
    .attr("class", TOOLTIP_CLASS)
    .style("opacity", 0);

  d3.select(targetSelector)
    .on("mouseover", function () {
      tooltip.transition()
        .duration(TOOLTIP_SHOW_DURATION)
        .style("opacity", 1);

      tooltip.html(tooltipMessage)
        .style("left", (d3.event.pageX + TOOLTIP_OFFSET_X) + "px")
        .style("top", (d3.event.pageY - TOOLTIP_OFFSET_Y) + "px");
    })
    .on("mouseout", function () {
      tooltip.transition()
        .duration(TOOLTIP_HIDE_DURATION)
        .style("opacity", 0);
    });
}

function update(Npapers, nodes, links) {
  const fieldOption = document.getElementById(CONSTANTS.FIELD_DROPDOWN_ID).value;
  const graphOption = document.getElementById(CONSTANTS.GRAPH_DROPDOWN_ID).value;
  debugger
  const filename = "../" + CONSTANTS.DATA_DIRECTORY + CONSTANTS.FREQ + CONSTANTS.ITEMS.get(fieldOption) + CONSTANTS.DAT_TYPE;
  loadFrequencyData(filename, (dataItems) => {
    d3.select(CONSTANTS.SORT_DROPDOWN_ID).on("change", () => renderList(dataItems, fieldOption, Npapers));
    renderList(dataItems, fieldOption, Npapers);
    draw_graph(fieldOption, graphOption, nodes, links);
  });
}

function loadFrequencyData(filename, callback) {
  d3.csv(filename, (error, csvData) => {
    if (error) {
      console.error("Error loading CSV:", error);
      return;
    }

    const dataItems = csvData.map((row, index) => [
      index + 1,
      row.citation_item,
      +row.item_count,
      +row.frequency
    ]);

    callback(dataItems);
  });
}

function renderList(dataItems, fieldOption, Npapers) {
  d3.select(CONSTANTS.NONE_AVAILABLE_ID).style("opacity", 0);
  const sortBy = document.getElementById(CONSTANTS.SORT_DROPDOWN_ID).value;
  const sortedData = sortDataItems(dataItems, sortBy);
  const tableHTML = generateTableHTML(sortedData, fieldOption, Npapers);

  d3.select(CONSTANTS.LIST_TAB_ID).html(tableHTML).property("scrollTop", 0);
}

function sortDataItems(dataItems, sortBy) {
  if (sortBy === CONSTANTS.SORT_OPTIONS[1].value) {
    return dataItems.sort((a, b) => b[1].toLowerCase() > a[1].toLowerCase() ? -1 : 1);
  } else if (sortBy === CONSTANTS.SORT_OPTIONS[1].value) {
    return dataItems.sort((a, b) => {
      if (a[2] === b[2]) {
        return b[1].toLowerCase() > a[1].toLowerCase() ? -1 : 1;
      }
      return b[2] - a[2];
    });
  }
  return dataItems;
}

function generateTableHTML(dataItems, fieldOption, Npapers) {
  const fontSize = CONSTANTS.TITLE_FONT_SIZE_DEFAULT;

  let table = `
    <table style="width:99%; table-layout:fixed; margin-left:1%; font-size:${fontSize}em;">
      <tr>
        <th align="left" style="width:7%;">${CONSTANTS.RANK_HEADER}</th>
        <th align="left" style="width:63%;">${CONSTANTS.ITEM_LABEL_PREFIX}${CONSTANTS.ITEMS[fieldOption]}</th>
        <th align="right" style="width:15%;">${CONSTANTS.RECORD_COUNT_HEADER}</th>
        <th align="right" style="width:15%;">${CONSTANTS.RECORD_PERCENT_HEADER}${Npapers}</th>
      </tr>`;
  dataItems.forEach(([rank, itemName, recordCount, percentage]) => {
    if (itemName === "none available") {
      displayNoDataMessage(percentage);
    } else {
      const displayPercentage = percentage < CONSTANTS.EPSILON_THRESHOLD ? CONSTANTS.EPSILON_SYMBOL : percentage;
      table += `
        <tr>
          <td>${rank}</td>
          <td style="width:63%;">${itemName}</td>
          <td align="right">${recordCount}</td>
          <td align="right">${displayPercentage}</td>
        </tr>`;
    }
  });

  table += `</table>`;
  return table;
}

function displayNoDataMessage(percentage) {
  d3.select(CONSTANTS.NONE_AVAILABLE_ID)
    .html(`${CONSTANTS.NO_DATA_NOTE_PREFIX}${percentage} ${CONSTANTS.NO_DATA_NOTE_SUFFIX}`)
    .style("opacity", 1);
}

function draw_graph(fieldOption, graphOption, nodes, links) {
  debugger
  if (graphOption === 'science') {
    GRAPHS.VIZscience(fieldOption);
    return;
  }

  if (graphOption === 'custom') {
    if (['DE', 'TI', 'CR'].includes(fieldOption)) {
      GRAPHS.VIZnetwork(fieldOption, nodes, links);
    } else if (['AU'].includes(fieldOption)) {
      GRAPHS.VIZwordcloud(fieldOption);
    } else if (fieldOption === 'CU') {
      GRAPHS.VIZmap(fieldOption);
    } else if (fieldOption === 'PY') {
      GRAPHS.VIZpubyears(fieldOption);
    } else if (['CR'].includes(fieldOption)) {
      GRAPHS.VIZpiechart(fieldOption);
    }
  }
}



