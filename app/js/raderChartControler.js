const firstRead = (callback) => {
  jQuery.getJSON("http://localhost:50001/api/product",
    function (data) {
      information = data["_items"];
      // nutrientがないものを除外
      for (let i = information.length - 1; 0 <= i; i--) {
        if (information[i]["nutrient"] == null) {
          information.splice(i, 1);
        }
      }
      console.log(information);
      callback()
    });
}
const secondRead = (callback) => {
  jQuery.getJSON("http://localhost:50001/api/nutrient",
    function (data) {
      nutrient = data["_items"][0]["nutrient"];
      console.log(nutrient);
      callback()
    });
}

function MakeIntersection(index_list, information, nutrient) {
  var intersection = [];
  var label = [];
  var tempNutrient = [];

  // 成分名リストを作成
  for (let i = 0; i < nutrient.length; i++) label.push(nutrient[i]["nutrient"]);

  for (let i = 0; i < index_list.length; i++) {
    intersection = [];
    for (let j = 0; j < information[index_list[i]]["nutrient"].length; j++) {
      let exist_index = -1;
      for (let k = 0; k < label.length; k++) {
        if (information[index_list[i]]["nutrient"][j]["nutrient"] == label[k]) {
          exist_index = k;
          break;
        }
      }
      if (-1 < exist_index && !intersection.includes(label[exist_index])) {
        intersection.push(label[exist_index]);
      }
    }
    label = intersection;
  }

  for (let i = 0; i < nutrient.length; i++)  if (intersection.includes(nutrient[i]["nutrient"])) tempNutrient.push(nutrient[i]);
  tempNutrient;

  return tempNutrient;
}

function MakeDataList(index_list, information, nutrient) {
  data = [];
  maxValue = 0;
  for (let i = 0; i < index_list.length; i++) {
    var tempData = [];
    for (let j = 0; j < information[index_list[i]]["nutrient"].length; j++) {
      let index = -1;
      for (let k = 0; k < nutrient.length; k++) {
        if (information[index_list[i]]["nutrient"][j]["nutrient"] == nutrient[k]["nutrient"]) {
          index = k;
          break;
        }
      }
      if (-1 < index) {
        temp = information[index_list[i]]["nutrient"][j]
        var axis = String(temp["nutrient"] + "[" + temp["unit"] + "]");
        var value = Number(information[index_list[i]]["nutrient"][j]["value"]) / Number(nutrient[index]["value"]);
        tempData.push({ "axis": axis, "value": value })
        console.log(tempData);
        // set maxValue
        if (maxValue < value) maxValue = value;
      }
    }

    data.push(tempData);
  }

  return [data, maxValue];
}

function MakeColorList(N) {
  colorList = [];
  for (let i = 0; i < N; i++) {
    color = hsv2rgb(i * (360 / N), 0.6, 1);
    colorList.push(color.hex);
  }
  console.log(colorList);
  return colorList;
}

// https://qiita.com/akebi_mh/items/3377666c26071a4284ee
function hsv2rgb(h, s, v) {
  // 引数処理
  h = (h < 0 ? h % 360 + 360 : h) % 360 / 60;
  s = s < 0 ? 0 : s > 1 ? 1 : s;
  v = v < 0 ? 0 : v > 1 ? 1 : v;

  // HSV to RGB 変換
  const c = [5, 3, 1].map(function (i) {
    return Math.round((v - Math.max(0, Math.min(1, 2 - Math.abs(2 - (h + i) % 6))) * s * v) * 255);
  });

  // 戻り値
  return {
    hex: '#' + (('00000' + (c[0] << 16 | c[1] << 8 | c[2]).toString(16)).slice(-6)),
    rgb: c, r: c[0], g: c[1], b: c[2],
  };
}

function MakeRaderChart() {

  // search intersection part & make new nutrient
  nutrient_intersection = MakeIntersection(index_list, information, nutrient);

  // make raderChart data
  [data, maxValue] = MakeDataList(index_list, information, nutrient_intersection);

  // make raderChart color
  var color_list = MakeColorList(index_list.length);
  var color = d3.scale.ordinal()
    .range(color_list);

  $("#legends").empty();
  document.getElementById("legends").style.height = 30 + 30 * index_list.length + "px";

  var svg = d3.select("#legends");
  for (let i = 0; i < index_list.length; i++) {
    svg.append("circle").attr("cx", 30).attr("cy", 30 + i * 30).attr("r", 6).style("fill", color_list[i]);
    svg.append("text").attr("x", 50).attr("y", 30 + i * 30).text(information[index_list[i]]["name"]).style("font-size", "15px").attr("alignment-baseline", "middle");
  }

  var radarChartOptions = {
    w: width,
    h: height,
    margin: margin,
    maxValue: maxValue,
    levels: 5,
    roundStrokes: true,
    color: color
  };
  //Call function to draw the Radar chart
  RadarChart(".radarChart", data, radarChartOptions);
}


// all information contain
var information;
// nutrients per day from: https://www.otsuka.co.jp/cmt/nutrition/1day/
var nutrient;
var nutrient_intersection;
var data;
var maxValue;
var colorList;
// target index, ex. dropdown
var index_list = [];

var margin = { top: 100, right: 100, bottom: 100, left: 100 },
  width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
  height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);

firstRead((firstValue) => {
  secondRead((secondValue) => {
    MakeRaderChart();

    // set select element
    for (let i = 0; i < information.length; i++) {
      $('#multiple').append($('<option>').attr({ value: i }).text(information[i]["name"]));
    }
    $('#select-all').click(function () {
      $('#multiple').selectMultiple('select_all');
      return false;
    });
    $('#deselect-all').click(function () {
      $('#multiple').selectMultiple('deselect_all');
      return false;
    });
    // set select search
    $('#multiple').selectMultiple({
      selectableHeader: "<input type='text' class='search-input selectableHeader' autocomplete='off' placeholder='商品検索'>",
      afterInit: function (ms) {
        var that = this,
          $selectableSearch = that.$selectableUl.prev(),
          selectableSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selectable';

        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
          .on('keydown', function (e) {
            if (e.which === 40) {
              that.$selectableUl.focus();
              return false;
            }
          });
      },
      afterSelect: function () {
        this.qs1.cache();
      },
      afterDeselect: function () {
        this.qs1.cache();
      }
    });
  })
})


// select box config
let select = document.getElementById("multiple");
select.onchange = event => {
  index_list = $("#multiple").val().map(str => parseInt(str, 10));

  MakeRaderChart();
}