const _location = window.location.href.split('/');
const CITY_ID = _location[_location.length - 2];
const BASE_URL = "/cities/api/";


const URL_GET_WORDS = `${BASE_URL}words/` + CITY_ID;
const URL_GET_STATS = `${BASE_URL}/stats/`;
const URL_GET_POSTS = `${BASE_URL}posts/` + CITY_ID;

google.charts.load('current', {'packages': ['line']});
google.charts.setOnLoadCallback(drawChart);

async function get_stats() {
    return fetch(URL_GET_POSTS)
        .then(data => {
            return data.json().then(
                json => {
                    return json
                }
            )
        })
}

console.log(get_words())

async function get_words() {
    return fetch(URL_GET_WORDS)
        .then(data => {
            return data.json().then(json => {
                return json
            })
        }).catch(e => {
            console.log(e)
        })
}

google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);

async function drawChart() {
    const scores = await get_stats();
    let total = [['Дата','Среднее значение']];


    for (i in scores) {
        const current = scores[i]
        total.push([new Date(current.date), current.avg_score])
    }




    let data = new google.visualization.arrayToDataTable(total, false);

    const options = {
                title: 'Среднее настроение в городе по датам',
                subtitle: '0 - самое негативное, 1 - самое позитивное',
                legend: {position: 'top'},

                histogram: {
                    minValue: 0,
                    maxValue: 1
                }
            };

    let formatter = new google.visualization.DateFormat({formatType: 'short'});
    formatter.format(data, 1);

    const chart = new google.visualization.ColumnChart(document.getElementById('avg_sentiment_city'));
    chart.draw(data, options);
}

async function set_words_cloud() {
    let myWords = await get_words();
    myWords = myWords.themes.split(',');

    const margin = {top: 10, right: 10, bottom: 10, left: 10},
        width = 450 - margin.left - margin.right,
        height = 450 - margin.top - margin.bottom;

    let svg = d3.select("#words_cloud").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


        function draw(words) {
            svg
                .append("g")
                .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", 20)
                .style("fill", "#69b3a2")
                .attr("text-anchor", "middle")
                .style("font-family", "Impact")
                .attr("transform", function (d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function (d) {
                    return d.text;
                });
        }

    var layout = d3.layout.cloud()
        .size([width, height])
        .words(myWords.map(function (d) {
            return {text: d};
        }))
        .padding(5)        //space between words
        .rotate(-45)       // rotation andgle in degrees
        .fontSize(20)      // font size of words
        .on("end", draw);

    layout.start();
}


set_words_cloud();

