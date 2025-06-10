import Fields from "../enum/FieldsEnumerator";
import * as d3 from 'd3';

export default class CorpusDescription {

    private readonly DATA_DIRECTORY = "newProject/vizualization/data/freqs/"
    private readonly JSON_TYPE = ".json"

    public doCDviz(){
        debugger
        //width stuff
        foo=d3.select('#headermenu').node().getBoundingClientRect().width-240
        d3.select("#container").style("width", foo+"px")
        d3.select("#redocloud").style("left", (250+0.40*foo)+"px")
        d3.select("#slider").style("left", (250+0.40*foo)+"px")
        //height stuff
        foo=window.innerHeight-50
        d3.select("#container").style("height", foo+"px")
        d3.select("#sidepanel").style("height", foo+"px")
        d3.select("#listTAB").style("height", (foo-42)+"px")
        d3.select("#graph").style("height", (foo-42)+"px").style("width", "100%")
        d3.select("#slider").style("top", (foo-20)+"px")
      
        var alpha = 0
        var filename = ''
        fields=['AU','CU','DT','I','K','LA','J','Y','R','RJ','S']; //['AK','AU','CU','DT','I','K','LA','J','Y','R','RJ','S','S2','TK'];
        graph_type=['custom','science'];
        items={'AU':'author','CU':'country/territory','I':'institution','DT':'document type','LA':'language','Y':'publication year','S':'subject category','S2':'subject subcategory','J':'publication source','K':'keyword','AK':'authors\' keyword','TK':'title word','R':'reference','RJ':'reference source'};
        itemsB={'AU':'authors','CU':'countries/territories','CI':'cities','I':'institutions','DT':'document types','LA':'languages','Y':'publication years','S':'subject categories','S2':'subject subcategories','J':'publication sources','K':'keywords','AK':'authors\' keywords','TK':'title words','R':'references','RJ':'reference sources'};
        file={'AU':'authors','CU':'countries','I':'institutions','DT':'doctypes','LA':'languages','Y':'years','S':'subjects','S2':'subjects2','J':'journals','K':'keywords','AK':'authorskeywords','R':'references','RJ':'refjournals'};
        file={'AU':'authors','CU':'countries','I':'institutions','DT':'doctypes','LA':'languages','Y':'years','S':'subjects','J':'journals','K':'keywords','AK':'authorskeywords','TK':'titlewords','R':'references','RJ':'refjournals'};
        country_code={'Canada': 'CAN', 'East Timor': 'TLS', 'Turkmenistan': 'TKM', 'United States of America': 'USA', 'United States': 'USA', 'Lithuania': 'LTU', 'Cambodia': 'KHM', 'Ethiopia': 'ETH', 'Swaziland': 'SWZ', 'Argentina': 'ARG', 'Bolivia': 'BOL', 'Cameroon': 'CMR', 'Burkina Faso': 'BFA', 'Ghana': 'GHA', 'Saudi Arabia': 'SAU', 'Slovenia': 'SVN', 'Guatemala': 'GTM', 'Bosnia and Herzegovina': 'BIH', 'Guinea': 'GIN', 'Germany': 'DEU', 'Spain': 'ESP', 'Liberia': 'LBR', 'Netherlands': 'NLD', 'Pakistan': 'PAK', 'Oman': 'OMN', 'Zambia': 'ZMB', 'Greenland': 'GRL', 'French Guiana': 'GUF', 'New Zealand': 'NZL', 'Yemen': 'YEM', 'Jamaica': 'JAM', 'Albania': 'ALB', 'West Bank': 'PSE', 'Nicaragua': 'NIC', 'United Arab Emirates': 'ARE', 'Uruguay': 'URY', 'India': 'IND', 'Azerbaijan': 'AZE', 'Lesotho': 'LSO', 'Republic of Serbia': 'SRB', 'Kenya': 'KEN', 'South Korea': 'KOR', 'Tajikistan': 'TJK', 'Turkey': 'TUR', 'Afghanistan': 'AFG', 'Bangladesh': 'BGD', 'Mauritania': 'MRT', 'Solomon Islands': 'SLB', 'Kyrgyzstan': 'KGZ', 'Mongolia': 'MNG', 'Mongol Peo Rep': 'MNG', 'France': 'FRA', 'Rwanda': 'RWA', 'Namibia': 'NAM', 'Somalia': 'SOM', 'Peru': 'PER', 'Laos': 'LAO', 'Norway': 'NOR', 'Malawi': 'MWI', 'Benin': 'BEN', 'Western Sahara': 'ESH', 'Cuba': 'CUB', 'Montenegro': 'MNE', 'Republic of the Congo': 'COG', 'Rep Congo': 'COG', 'Togo': 'TGO', 'China': 'CHN', 'Peoples R China': 'CHN', 'Armenia': 'ARM', 'Dominican Republic': 'DOM', 'Ukraine': 'UKR', 'Somaliland': '-99', 'Finland': 'FIN', 'Libya': 'LBY', 'Indonesia': 'IDN', 'Central African Republic': 'CAF', 'Cent Afr Republ': 'CAF', 'United States': 'USA', 'Sweden': 'SWE', 'Belarus': 'BLR', 'Mali': 'MLI', 'Russia': 'RUS', 'Bulgaria': 'BGR', 'Romania': 'ROU', 'Angola': 'AGO', 'Portugal': 'PRT', 'Trinidad and Tobago': 'TTO', 'Cyprus': 'CYP', 'Qatar': 'QAT', 'Malaysia': 'MYS', 'Austria': 'AUT', 'Vietnam': 'VNM', 'Mozambique': 'MOZ', 'UK': 'GBR', 'Hungary': 'HUN', 'Niger': 'NER', 'Brazil': 'BRA', 'Falkland Islands': 'FLK', 'The Bahamas': 'BHS', 'Panama': 'PAN', 'Guyana': 'GUY', 'Costa Rica': 'CRI', 'Luxembourg': 'LUX', 'Ivory Coast': 'CIV', 'Cote Ivoire':'CIV', 'Nigeria': 'NGA', 'Ecuador': 'ECU', 'Czech Republic': 'CZE', 'Brunei': 'BRN', 'Australia': 'AUS', 'Iran': 'IRN', 'USA': 'USA', 'Algeria': 'DZA', 'El Salvador': 'SLV', 'Chile': 'CHL', 'Puerto Rico': 'PRI', 'Belgium': 'BEL', 'Thailand': 'THA', 'Haiti': 'HTI', 'Belize': 'BLZ', 'Sierra Leone': 'SLE', 'Georgia': 'GEO', 'Gambia': 'GMB', 'Philippines': 'PHL', 'Guinea Bissau': 'GNB', 'Moldova': 'MDA', 'Morocco': 'MAR', 'Croatia': 'HRV', 'United Republic of Tanzania': 'TZA', 'Tanzania': 'TZA', 'Switzerland': 'CHE', 'Iraq': 'IRQ', 'Chad': 'TCD', 'Estonia': 'EST', 'Kosovo': '-99', 'Mexico': 'MEX', 'Lebanon': 'LBN', 'Northern Cyprus': '-99', 'South Africa': 'ZAF', 'Uzbekistan': 'UZB', 'Tunisia': 'TUN', 'Djibouti': 'DJI', 'Colombia': 'COL', 'Burundi': 'BDI', 'Slovakia': 'SVK', 'Taiwan': 'TWN', 'Fiji': 'FJI', 'Madagascar': 'MDG', 'Italy': 'ITA', 'Bhutan': 'BTN', 'Sudan': 'SDN', 'Nepal': 'NPL', 'Democratic Republic of the Congo': 'COD', 'Dem Rep Congo': 'COD', 'Suriname': 'SUR', 'Kuwait': 'KWT', 'Israel': 'ISR', 'Iceland': 'ISL', 'Venezuela': 'VEN', 'Senegal': 'SEN', 'Papua New Guinea': 'PNG', 'Zimbabwe': 'ZWE', 'Jordan': 'JOR', 'Vanuatu': 'VUT', 'Denmark': 'DNK', 'Kazakhstan': 'KAZ', 'Poland': 'POL', 'Eritrea': 'ERI', 'Ireland': 'IRL', 'Uganda': 'UGA', 'New Caledonia': 'NCL', 'Macedonia': 'MKD', 'North Korea': 'PRK', 'Paraguay': 'PRY', 'Latvia': 'LVA', 'South Sudan': 'SSD', 'Japan': 'JPN', 'Syria': 'SYR', 'Honduras': 'HND', 'Myanmar': 'MMR', 'Equatorial Guinea': 'GNQ', 'Egypt': 'EGY', 'French Southern and Antarctic Lands': 'ATF', 'United Kingdom': 'GBR', 'Antarctica': 'ATA', 'Greece': 'GRC', 'Sri Lanka': 'LKA', 'Gabon': 'GAB', 'Botswana': 'BWA'}
      
        // // input some general data
        d3.json(this.DATA_DIRECTORY+'DISTRIBS_itemuse'+this.JSON_TYPE, (data: any) => {
          Npapers=data.N;
          probability_count_value = makeCountValue(data);
          probability_cumulative_count = makeCumulativeValue(data);
          d3.json(dirdatafreqs+'coocnetworks.json', function(data) {Znodes = data.nodes; Zlinks = data.links; dotheviz();})
        })
      
      }

    private makeCountValue(data: any) {
        const probability_count_value = new Map();
        for (const value of Fields.LABELS()) {
          const countValueFieldName = `${value}_count_value`;
          probability_count_value.set(value, data[countValueFieldName]);
        }
        return probability_count_value;
      }
      
      private makeCumulativeValue(data: any) {
        const probability_cumulative_count = new Map();
        for (const value of Fields.LABELS()) {
          const cumulativeCountFieldName = `${value}_cumulative_count`;
          probability_cumulative_count.set(value, data[cumulativeCountFieldName]);
        }
        return probability_cumulative_count;
      }
}