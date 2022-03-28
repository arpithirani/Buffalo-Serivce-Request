function plotDonut(content){
   let data =JSON.parse(content)
   let s = data[0]["name"];
   let f = data[data.length-1]["name"];
   let layout = {
       title: 'Buffalo Service Requests by Department<br>'+s+" - "+f,
       showlegend: true,
       grid: {rows: 1, columns: data.length}
    };
  Plotly.newPlot("donut", data, layout);
}

function sendDonutData(){
  let st_year = document.getElementById("startYear")
  let st_value = st_year.value;
  let en_year = document.getElementById("endYear")
  let en_value = en_year.value;
  let dict = JSON.stringify({"year_start" : Number(st_value), "year_end" : Number(en_value)});
  st_year.value='';
  en_year.value='';
  ajaxPostRequest("/donut_chart", dict, plotDonut);
}


function plotScatter(content){
  let data = JSON.parse(content);
  let year = data["year"]
  let lay = {
     xaxis: { autorange: true },
     yaxis: { type: 'log', autorange: true },
     title: 'Service Request Duration by Department in ' + year
  };
  Plotly.newPlot("scatter", data["data"], lay);
}

function sendScatterData(){
  let num = document.getElementById("year").value;
  let dic = JSON.stringify({"year" : Number(num)});
  document.getElementById("year").value='';
  ajaxPostRequest("scatter_plot", dic, plotScatter); 
}