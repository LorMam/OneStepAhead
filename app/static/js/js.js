"use strict";
httpGetCsvStruct(loadGraphs, "/graphs");

httpGetCsvArray(loadParameters, "/parameter", 0, 1, 2, 3);

httpGetCsvArrayTable(gotFinalCleanData, '/finalCleanData');

const countryPlotter = new Plotter(document.getElementById("graphs"), "Days since 100 conf. Cases", "Confirmed Cases", (e) => "Day " + e, (e) => e + " Conf. Cases");

const predictionPlotter = new Plotter(document.getElementById("predictionCanvas"), "Days", "Predicted Cases", (e) => "Day " + e, (e) => e + " Confirmed Cases");

let countries = {};

let hoverable = true;

function createCountries(struct){
    let count = 0;
    let text = "";
    for (const [key, val] of Object.entries(struct)) {
        if(val[0] !== ""){
            countries[key] = true;
            text += ("<div class='noselect selected countryElement" + (count%2===0 ? " zebra" : "") + "' id='" + key + "' onmouseover='countryHovered(\"" + key + "\")' onclick='countryClicked(\"" + key + "\")'>" + key + "<img src='/static/img/Black_check.svg' class='countryCheck'></div>");
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
    countryPlotter.setVisibleOfGraph(country, visible, draw);
}

let timeout;
function countryHovered(country){
   clearTimeout(timeout);
   if(hoverable){
        timeout = setTimeout(() => {countryPlotter.hoverGraph(country);}, 100);
    }
}

function loadGraphs(struct){
    delete struct["Days since 100"];
    createCountries(struct);
    countryPlotter.setData(struct, (me, x) => {
        const date = new Date(me.values[0]);
        date.setDate(date.getDate() + x);
        return me.name + " (On date: " + ((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '.' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '.' + date.getFullYear() + ")";
    });
    countryPlotter.setKeyFilter(e => e !== "0");
}

function check(){
    for (let [key, val] of Object.entries(countries)) {
        val = true;
        setVisibilityOfCountry(key, true, false);
    }
    countryPlotter.draw();
}

function uncheck(){
    for (let [key, val] of Object.entries(countries)) {
        val = false;
        setVisibilityOfCountry(key, false, false);
    }
    countryPlotter.draw();
}

function resize(){
    countryPlotter.canvas.width = window.innerWidth * 0.68;
    countryPlotter.draw();
    predictionPlotter.canvas.width = window.innerWidth * 0.68;
    predictionPlotter.draw();
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
    hoverable = false;
    setTimeout(() => hoverable = true,200);
    let s = document.getElementById("search").value;
    for (const [key, val] of Object.entries(countries)) {
        if(key.toLowerCase().includes(s.toLowerCase(), 0)){
            document.getElementById(key).scrollIntoView({behavior: "smooth", block: "start"});
            document.getElementById("scrollPoint").scrollIntoView(true);
            window.scrollY += 100;
            countryPlotter.hoverGraph(key);
            return;
        }
    }
}


function logChanged(){
    countryPlotter.logaRythmus = document.getElementById("logCheck").checked;
    countryPlotter.draw();
}



let parameters = {};
let parameterPresets ={ "Recommended" : ["eProsperity Index Health Scor", "Education Index"]};

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
    loadParameterPreset(parameterPresets["Recommended"]);
    sendParameters();
    updateZebraParameters();
}

function loadParameterPreset(preset){
    for (let [key, val] of Object.entries(parameters)) {
        if(preset.includes(key)){
            selectParameter(key, false);
        }else {
            deselectParameter(key, false);
        }
    }
}

function selectParameter(name, setPreset){
    parameters[name] = true;
    document.getElementById(name + "unselected").style.display = "none";
    document.getElementById(name + "selected").style.display = "block";
    if(setPreset &&  !parameterPresets[document.getElementById("presetSelect").value].includes(name)) {
        parameterPresets[document.getElementById("presetSelect").value].push(name);
    }
    unloadParameters();
    updateZebraParameters()
}

function deselectParameter(name, setPreset) {
    parameters[name] = false;
    document.getElementById(name + "unselected").style.display = "block";
    document.getElementById(name + "selected").style.display = "none";
    if (setPreset && parameterPresets[document.getElementById("presetSelect").value].indexOf(name) !== -1) {
        parameterPresets[document.getElementById("presetSelect").value].splice(parameterPresets[document.getElementById("presetSelect").value].indexOf(name), 1);
    }
    unloadParameters();
    updateZebraParameters()
}

function paramClicked(name){
    if(parameters[name]){
        deselectParameter(name, true)
    }else{
        selectParameter(name, true);
    }
}

function getParameterList(){
    let list = "";
    for (const [key, val] of Object.entries(parameters)) {
        if (val) {
            list += key + ","
        }
    }
    return list.substring(0, list.length - 1);
}

function sendParameters(){
    let list = getParameterList();
    if(list.length > 0) {
        httpGetCsvArrayRowCol(gotParameters, "/getModel?parameterList=" + list, 1, 10, 0, 0);
    }else{
         document.getElementById("accuracy").innerText = "please select at least one Parameter";
    }
}

function unloadParameters(){
     document.getElementById("accuracy").innerText = "Click \"Make\" to refresh parameters";
    for (const key of Object.keys(parameters)) {
        document.getElementById(key + "selected").classList.remove("expandedParameter");
        document.getElementById(key + "selected").innerHTML = key;
    }
}

function gotParameters(result){
    unloadParameters();
    document.getElementById("accuracy").innerText = "Accuracy: " + Math.round(result[2][0] * 1000000) / 1000000;
    for (const parameter of result[0]) {
        if (parameter !== "\r" && parameter.length > 0){
            document.getElementById(parameter + "selected").classList.add("expandedParameter");
            document.getElementById(parameter + "selected").innerHTML = "" +
                parameter +
                "<hr>" +
                "Influence: " + Math.round(result[1][result[0].indexOf(parameter)] * 10000000) / 10000000 +
                "<img src='/static/img/Black_check.svg' class='paramCheck invisible' alt='checkImage'>";
        }
    }
    predictCases(calculateGrowthRate(result));
}

function refreshPreset(){
    for (const [key, val] of Object.entries(parameters)) {
        if(val){
            selectParameter(key, true);
        }else{
            deselectParameter(key, true);
        }
    }
}

function removePreset(){
    let x = document.getElementById("presetSelect");
    x.remove(x.selectedIndex);
    delete parameterPresets[document.getElementById("presetSelect").value];
}

function addPreset(){
    const option = document.createElement("option");
    const text = "Preset0" + document.getElementById("presetSelect").options.length;
    option.text = text;
    document.getElementById("presetSelect").add(option);
    document.getElementById("presetSelect").value = text;
    parameterPresets[text] = [];
    refreshPreset();
}

function updateZebraParameters(){
    for (let i = 0; i < document.getElementById("parameterSelected").childNodes.length; i++) {
        if(i % 2 === 0){
            document.getElementById("parameterSelected").childNodes[i].classList.remove("parameterZebra");
        }else{
            document.getElementById("parameterSelected").childNodes[i].classList.add("parameterZebra");
        }
    }
    for (let i = 0; i < document.getElementById("parameterUnselected").childNodes.length; i++) {
        if(i % 2 === 0){
            document.getElementById("parameterUnselected").childNodes[i].classList.remove("parameterZebra");
        }else{
            document.getElementById("parameterUnselected").childNodes[i].classList.add("parameterZebra");
        }
    }
}

let finalCleanData;
function gotFinalCleanData(struct){
    console.log(struct);
    finalCleanData = struct;
}

function calculateGrowthRate(result){
    console.log(result);
    for (let i = 0; i < 1; i++) {
        
    }
}

function presetChanged(){
    loadParameterPreset(parameterPresets[document.getElementById("presetSelect").value]);
}

//TODO @Lorenz function (grothrate) => Object{0: "100", 1: "109", 2: "169", 3: "200", 4: "239", 5: "267", 6: "314", 7: "314", 8: "559", 9: "689", … }
function predictCases(growthRate){
    let graph = {};
    graph[0] = 100;
    graph[1] = 200;
    //console.log(graph);
    return graph;
}