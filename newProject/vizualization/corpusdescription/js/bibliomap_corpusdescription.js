/* ---------------------------------------------------------------------------
   (c) BiblioMaps, 2017
   Author: Sebastian Grauwin
   website: sebastian-grauwin.com
   --------------------------------------------------------------------------- */

/*-------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------------------------------------------------------------*/
import * as CONSTANTS from '/newProject/vizualization/corpusdescription/js/constants.js';

export function doCDviz(){
  debugger
  makeGraphWitzWindow()
  d3.json("../" + CONSTANTS.DATA_DIRECTORY + CONSTANTS.DISTRIBUTION_FILE, function(data) {
    const Npapers = data.N;
    var probability_count_value = makeCountValue(data);
    var probability_cumulative_count = makeCumulativeValue(data);
    d3.json("../" + CONSTANTS.DATA_DIRECTORY + CONSTANTS.COORELATION_FILE, function(data) {
      const nodes = data.nodes;
      const links = data.links;
      makeSideBarMenu(Npapers);
    });
  });
}

function makeSideBarMenu(numPublications) {
  const NUM_PUB_ID = '#NUMPUB';
  const GRAPH_PTIONS = [
    { value: 'custom', text: 'Custom', selected: true },
    { value: 'science', text: 'Distributions', selected: false }
  ];
  itemOptions = setupItemDropdown(CONSTANTS.ITEMS.keys(), CONSTANTS.ITEMS, selectedField);
  createSelectHTML(CONSTANTS.ITEM_SELECTION_ID, itemOptions);
  d3.select(CONSTANTS.ITEM_SELECTION_ID).html(createSelectHTML(CONSTANTS.FIELD_DROPDOWN_ID, itemOptions));
  d3.select(`#${CONSTANTS.FIELD_DROPDOWN_ID}`).on('change', update);
  d3.select(CONSTANTS.GRAPH_SELECTION_ID).html(createSelectHTML(CONSTANTS.GRAPH_DROPDOWN_ID, CONSTANTS.graphOptions));
  d3.select(`#${CONSTANTS.GRAPH_DROPDOWN_ID}`).on('change', update);
  d3.select(CONSTANTS.SORT_TAB_ID).html(createSelectHTML(CONSTANTS.SORT_DROPDOWN_ID, CONSTANTS.SORT_OPTIONS));
  d3.select(NUM_PUB_ID).html(numPublications);
  initializeTooltips();
}

function createSelectHTML(id, options) {
  return `
    <select id="${id}" style="${CONSTANTS.SELECT_WIDTH_STYLE}">
      ${options.map(object =>
        `<option value="${object.value}" ${object.selected ? 'selected' : ''}>${object.text}</option>`
      ).join('')}
    </select>
  `;
}

function setupItemDropdown(fields, items, selectedField) {
  return fields.map(f => ({
    value: f,
    text: capitalizeFirstLetter(items[f]),
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
    prep_infobulle(selector, message);
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

function update() {
  fieldOption = document.getElementById(CONSTANTS.FIELD_DROPDOWN_ID).value;
  graphOption = document.getElementById(CONSTANTS.GRAPH_DROPDOWN_ID).value;
  const filename = file[fieldOption];

  loadFrequencyData(filename, (dataItems) => {
    d3.select(CONSTANTS.SORT_DROPDOWN_ID).on("change", () => renderList(dataItems));
    renderList(dataItems);
    draw_graph(0, fieldOption, graphOption);
  });
}

function loadFrequencyData(filename, callback) {
  d3.csv(`${CONSTANTS.DATA_DIRECTORY}freq_${filename}.dat`, (error, csvData) => {
    if (error) {
      console.error("Error loading CSV:", error);
      return;
    }
    const dataItems = csvData.map((row, index) => [
      index + 1, row.item, +row.count, +row.f
    ]);
    callback(dataItems);
  });
}

function renderList(dataItems) {
  d3.select(CONSTANTS.NONE_AVAILABLE_ID).style("opacity", 0);

  const sortBy = document.getElementById(CONSTANTS.SORT_TAB_ID).value;
  const sortedData = sortDataItems(dataItems, sortBy);
  const tableHTML = generateTableHTML(sortedData);

  d3.select(CONSTANTS.LIST_TAB_ID).html(tableHTML).property("scrollTop", 0);
}

function sortDataItems(dataItems, sortBy) {
  if (sortBy === CONSTANTS.SORT_OPTIONS[1].value) {
    return dataItems.sort((a, b) => b[1].toLowerCase() > a[1].toLowerCase() ? -1 : 1);
  } else if (sortBy === CONSTANTS.SORT_OPTIONS[2].value) {
    return dataItems.sort((a, b) => {
      if (a[2] === b[2]) {
        return b[1].toLowerCase() > a[1].toLowerCase() ? -1 : 1;
      }
      return b[2] - a[2];
    });
  }
  return dataItems;
}

function generateTableHTML(dataItems) {
  const fontSize = fieldOption.includes("R") ? CONSTANTS.TITLE_FONT_SIZE_FOR_R : CONSTANTS.TITLE_FONT_SIZE_DEFAULT;

  let table = `
    <table style="width:99%; table-layout:fixed; margin-left:1%; font-size:${fontSize}em;">
      <tr>
        <th align="left" style="width:7%;">${CONSTANTS.RANK_HEADER}</th>
        <th align="left" style="width:63%;">${CONSTANTS.ITEM_LABEL_PREFIX}${items[fieldOption]}</th>
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

function draw_graph(fieldOption, graphOption) {
  if (graphOption === 'science') {
    VIZscience();
    return;
  }

  if (graphOption === 'custom') {
    if (['DE', 'TI', 'CR'].includes(fieldOption)) {
      VIZnetwork();
    } else if (['AU'].includes(fieldOption)) {
      VIZwordcloud();
    } else if (fieldOption === 'CU') {
      VIZmap();
    } else if (fieldOption === 'PY') {
      VIZpubyears();
    } else if (['CR'].includes(fieldOption)) {
      VIZpiechart();
    }
  }
}

function resetGraphArea() {
  d3.select("#graph").html('').style("background", 'white');
  d3.select("#slider").html('');
  d3.select("#redocloud").html('');
  d3.select("#custominfo").html("").style("opacity", 0);
}

function getChartDimensions(isMultiItem) {
  const graphBox = d3.select('#graph').node().getBoundingClientRect();
  const marginTopExtra = isMultiItem ? 0 : graphBox.height * 0.2;
  const heightFactor = isMultiItem ? 0.5 : 0.7;

  const margin = {
    top: 30 + marginTopExtra,
    right: 100,
    bottom: 60,
    left: 120
  };

  const width = graphBox.width - margin.left - margin.right;
  const height = graphBox.height * heightFactor - margin.top - margin.bottom;

  return { margin, width, height };
}

function showTooltip(text, event) {
  d3.select("#tooltip")
    .transition().duration(200).style("opacity", .95)
    .text(text)
    .style("left", (event.pageX - 155) + "px")
    .style("top", (event.pageY - 20) + "px");
}

