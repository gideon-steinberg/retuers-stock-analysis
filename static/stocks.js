function update_td_style(td, mean, mean_difference){
  if(mean <= 2){
    td.css("background-color", "#00ff00");
  }
  if (mean >= 3){
    td.css("background-color", "#ff0000");
    td.css("color","#ffffff");
  }
  if (mean_difference <= -1){
    td.css("font-weight", "bold");
  }
}

function create_td(tr, data, to_style, to_center){
  var td = $(document.createElement("td"));
  if (to_style === true){
    update_td_style(td, data.mean, data.mean_difference);
  }
  if(to_center === true){
      td.attr("class", "text-center");
  }
  tr.append(td);
  return td;
}

function create_link_ref(tr, data){
  var td = create_td(tr, data, false, false);
  var a_ref = $(document.createElement("a"));
  a_ref.attr("href","http://www.reuters.com/finance/stocks/analyst?symbol="+data.code);
  a_ref.html(data.code);
  td.append(a_ref);
}

function create_remove_button(tr, data){
  var td = create_td(tr, data, false, false);
  var form = $(document.createElement("form"));
  var input = $(document.createElement("input"));
  var button = $(document.createElement("button"));
  var span = $(document.createElement("span"));
  
  form.attr("action", "remove_stock");
  
  input.attr("type", "hidden");
  input.attr("name", "stock");
  input.attr("value", data.code);
  
  button.attr("type", "submit");
  button.attr("class", "btn btn-default");
  
  span.attr("class", "glyphicon glyphicon-minus text-danger");
  button.html("&nbsp;");
  
  button.append(span);
  form.append(input);
  form.append(button);
  td.append(form);
}

function create_tr(data) {
  var tbody = $("tbody.stock-tbody");
  data = JSON.parse(data);
  var tr = $(document.createElement("tr"));
  
  // create all the data elements
  create_td(tr, data, true, false).html(data.code);
  create_td(tr, data, true, false).html(data.description);
  create_td(tr, data, true, true ).html(data.buy);
  create_td(tr, data, true, true ).html(data.outperform);
  create_td(tr, data, true, true ).html(data.hold);
  create_td(tr, data, true, true ).html(data.underperform);
  create_td(tr, data, true, true ).html(data.sell);
  create_td(tr, data, true, true ).html(data.mean);
  create_td(tr, data, true, true ).html(data.mean_difference);
  create_td(tr, data, true, false).html(data.consensus);
  create_td(tr, data, true, true ).html(data.dividend);
  create_td(tr, data, true, true ).html(data.price_earnings);
  create_link_ref(tr, data);
  create_remove_button(tr, data);
  
  tbody.append(tr);
}

function parse_stock_list(data){
  var stocks = [];
  var i = 0;
  data = JSON.parse(data);
  var length = data.length;
  
  for (i = 0; i < length; i++) {
    stocks.push(data[i]); 
  }
  
  length = stocks.length;
  
  for (i = 0; i < length; i++) {
    $.ajax({
      url: "/stocks/stock_info?stock="+stocks[i],
    }).done(create_tr);
  }
  
}

$( document ).ready(function() {
   $.ajax({
      url: "/stocks/stock_list",
    }).done(parse_stock_list); 
});