"use strict";
//httpGetCsvStruct(loadGraphs, "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv");
httpGetCsvStruct(loadGraphs, "https://raw.githubusercontent.com/ChristophAl/OneStepAhead/master/DataProcessing/PipelineIntermediates/CountryCasesFromHopkins.csv");

httpGetCsvArray(loadParameters, "/graphs");

const plotter = new Plotter(document.getElementById("graphs"));

let countries = {};

let parameters = {};

function createCountries(struct){
    let count = 0;
    let text = "";
    for (const [key, val] of Object.entries(struct)) {
        if(val[0] != ""){
            countries[key] = true;
            text += ("<div class='noselect selected countryElement" + (count%2==0 ? " zebra" : "") + "' id='" + key + "' onmouseover='countryHovered(\"" + key + "\")' onclick='countryClicked(\"" + key + "\")'>" + key + "<img src='/static/img/Black_check.svg' class='countryCheck'></div>");
            count++;
        }
    }
    document.getElementById("countryList").innerHTML = text;
}

function countryClicked(country){
    countries[country] = !countries[country];
    setVisibilityOfCountry(country, countries[country], true);
}

function setVisibilityOfCountry(country, visible, draw){
    countries[country] = visible;
    if(visible){
        document.getElementById(country).classList.add("selected");
    }else {
        document.getElementById(country).classList.remove("selected");
    }
    plotter.setVisibleOfGraph(country, visible, draw);
}

function countryHovered(country){
    plotter.hoverGraph(country);
}

function loadGraphs(struct){
    createCountries(struct);
    plotter.setData(struct);
    plotter.setKeyFilter(e => e !="0");
}

function check(){
    for (let [key, val] of Object.entries(countries)) {
        val = true;
        setVisibilityOfCountry(key, true, false);
    }
    plotter.draw();
}

function uncheck(){
    for (let [key, val] of Object.entries(countries)) {
        val = false;
        setVisibilityOfCountry(key, false, false);
    }
    plotter.draw();
}

function resize(){
    plotter.canvas.width = window.innerWidth * 0.68;
    plotter.draw();
}

window.onresize = resize;
resize();

let firstScrolled = false;
let images = 8;
//              startOffset     offsetOfVisibility  time remaining
//                              after start anim    visible
let timing = [  2000,           2000,               7000];
setTimeout(function(){startGraph(0)}, timing[0]);
setTimeout(function(){startGraph(3)}, timing[0] + 2000);
setTimeout(function(){startGraph(6)}, timing[0] + 4000);
function startGraph(start){
    let self = start;
    setTimeout(function(){stopGraph(self);}, timing[1]);
    start = (start + 1) % images;
    document.getElementById("loading" + start).classList.add("loadAnimation");
    startVisibleGraph(start);
}

function stopGraph(self){
    document.getElementById("loading" + self).classList.remove("loadAnimation");
}

function startVisibleGraph(self){
    document.getElementById("loading" + self).classList.add("loadVisible");
    setTimeout(function(){stopVisibleGraph(self);}, timing[2]);
}

function stopVisibleGraph(self){
    document.getElementById("loading" + self).classList.remove("loadVisible");
    startGraph(self);
}

//3D effect
window.addEventListener("scroll", handleScroll);
handleScroll();
function handleScroll(){
    firstScrolled = true;
    let scrollY = window.scrollY;
    if(scrollY >= window.innerHeight){
        document.getElementById("nav").classList.add("navVisible");
    }else{
        document.getElementById("nav").classList.remove("navVisible");
    }
    document.getElementById("headLine").style.top = 45 - (scrollY / window.innerHeight * 50) + "vh";
    for(let i = 0; i < images; i ++){
        document.getElementById("loading" + i).style.top = -scrollY / (2.2 + (i % 4)) + "px";
    }
}

function search(){
    let s = document.getElementById("search").value;
    for (const [key, val] of Object.entries(countries)) {
        if(key.toLowerCase().includes(s.toLowerCase(), 0)){
            document.getElementById(key).scrollIntoView(true);
            document.getElementById("graphs").scrollIntoView(true);
            return;
        }
    }
}

function loadParameters(params){
    let text = "";
    let text1 = "";
    for (const param of params) {
        parameters[param] = false;
        text += "<div class='parameter noselect' id='" + param + "unselected' onclick='paramClicked(\"" + param + "\")'><span>" + param + "</span></div>"
        text1 += "<div class='parameter noselect' id='" + param + "selected' onclick='paramClicked(\"" + param + "\")' style='display: none;'>" + param + "<img src='/static/img/Black_check.svg' class='paramCheck'></div>"
    }
    document.getElementById("parameterUnselected").innerHTML = text;
    document.getElementById("parameterSelected").innerHTML = text1;
}

function paramClicked(name){
    parameters[name] = !parameters[name];
    if(parameters[name]){
        document.getElementById(name + "unselected").style.display = "none";
        document.getElementById(name + "selected").style.display = "block";
    }else{
        document.getElementById(name + "unselected").style.display = "block";
        document.getElementById(name + "selected").style.display = "none";
    }
}