"use strict";
httpGetCsvStruct(loadGraphs, "static/data/CountryCasesFromHopkins.csv");

httpGetCsvArray(loadParameters, "/parameter", 0, 1, 2, 3);

httpGetCsvArrayTable(gotFinalCleanData, '/finalCleanData');

const countryPlotter = new Plotter(document.getElementById("graphs"), "Days since 100 conf. Cases", "Confirmed Cases", (e) => "Day " + e, (e) => e + " Conf. Cases");

const predictionPlotter = new Plotter(document.getElementById("predictionCanvas"), "Days", "Predicted Cases", (e) => "Day " + e, (e) => Math.round(e) + " Predicted Cases");

let countries = {};

let maxCasesForPredict = 200;
let predictableCountries = [];

let hoverable = true;

//crate countryList
function createCountries(struct){
    //createPredictableCountries(struct);
    let count = 0;
    let text = "";
    for (const [key, val] of Object.entries(struct)) {
        if(val[0] !== ""){
            let color = getRandomColor();
            for (const graph of countryPlotter.graphs) {
                if(graph.name === key){
                    color = graph.color;
                }
            }
            countries[key] = true;
            text += ("<div onclick='countryClicked(\"" + key + "\")' class='noselect selected countryElement" + (count%2===0 ? " zebra" : "") + "' id='" + key + "'><img src='static/img/search.svg' height='20px' width='auto' onmouseleave='countryLeave();' onclick='countryHovered(\"" + key + "\"); countryPlotter.clickGraph(\"" + key + "\");' style='background-color: " + color + "; margin-right: 10px;' alt='search country'>" + key + "<img style='margin-right: 6px;' height='20px' width='auto' src='/static/img/eye.svg' class='countryCheck' alt='check'></div>");
            count++;
        }
    }
    document.getElementById("countryList").innerHTML = text;
}

//create dropdown for all predictable countrys. not in use yet
function createPredictableCountries(struct){
    for (const [country, cases] of Object.entries(struct)) {
        let max = 0;
        for (const value of Object.values(cases)) {
            max = Math.max(max, value)
        }
        if(max <= maxCasesForPredict){
            predictableCountries.push(country);
        }
    }
    createPredictableCountryDropDown();
}

//TODO proper prediction country loading
//create dropdown for all predictable countrys. only for testing purposes
function createPredictableCountriesTest(struct){
    predictableCountries = [];
    for (const country of Object.keys(struct)) {
        if(country !== "undefined" && country !== "Country"){
            predictableCountries.push(country);
        }
    }
    createPredictableCountryDropDown();
}

function createPredictableCountryDropDown(){
    let select = document.getElementById("predictCountrySelect");
    for (const country of predictableCountries) {
        let option = document.createElement("option");
        option.text = country;
        select.add(option);
    }
}

//toggle visibility from country
function countryClicked(country){
    countries[country] = !countries[country];
    setVisibilityOfCountry(country, countries[country], true);
}

//set visible of country x
function setVisibilityOfCountry(country, visible, draw){
    countries[country] = visible;
    if(visible){
        document.getElementById(country).classList.add("selected");
    }else {
        document.getElementById(country).classList.remove("selected");
    }
    countryPlotter.setVisibleOfGraph(country, visible, draw);
}

//finding country after hovering
//let timeout;
function countryHovered(country){
  // clearTimeout(timeout);
  // if(hoverable){
        //timeout = setTimeout(() => {countryPlotter.hoverGraph(country);}, 0);
   // }
    event.stopPropagation();
    countryPlotter.hoverGraph(country);
}

function countryLeave(){
    countryPlotter.grayAllIn();
    countryPlotter.draw();
}

//load country graphs from struct
function loadGraphs(struct){
    delete struct["Unnamed: 0"];
    delete struct["Days since 100"];
    countryPlotter.setData(struct, (me, x) => {
        const date = new Date(me.values[0]);
        date.setDate(date.getDate() + x);
        return me.name + " (On date: " + ((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '.' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '.' + date.getFullYear() + ")";
    });
    countryPlotter.setKeyFilter(e => e !== "0");
    createCountries(struct);
}

//show country
function check(){
    for (let [key, val] of Object.entries(countries)) {
        val = true;
        setVisibilityOfCountry(key, true, false);
    }
    countryPlotter.draw();
}

//hide country
function uncheck(){
    for (let [key, val] of Object.entries(countries)) {
        val = false;
        setVisibilityOfCountry(key, false, false);
    }
    countryPlotter.draw();
}

//resize handling
function resize(){
    countryPlotter.canvas.width = window.innerWidth * 0.68;
    countryPlotter.draw();
    predictionPlotter.canvas.width = window.innerWidth * 0.55;
    predictionPlotter.draw();
}

window.onresize = resize;
resize();

let firstScrolled = false;
let images = 9;
//everything related to the loading graph images
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
        document.getElementById("loading" + i).style.top = -scrollY / (2.1 + (i % 4)) + "px";
    }
    if(scrollY > (window.innerHeight / 3)){
        document.getElementsByClassName("scroll")[0].classList.add("invisible");
    }else {
        document.getElementsByClassName("scroll")[0].classList.remove("invisible");
    }
}

//search for country
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

// toggle logarythmic for counntry graph
function logChanged(){
    countryPlotter.logaRythmus = document.getElementById("logCheck").checked;
    countryPlotter.draw();
}



//Everything related to the prediction parameters

let parameters = {};
let parameterPresets ={ "Recommended" : ["Prosperity Index Health Score","Population using at least basic drinking-water services (%)","Human development index (HDI)","Population. total (millions)Population. under age 5 (%)","Population. ages 65 and older (%),yearly anual Temperature"]};

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

//idk
function getParameterList(){
    let list = "";
    for (const [key, val] of Object.entries(parameters)) {
        if (val) {
            list += key + ","
        }
    }
    return list.substring(0, list.length - 1);
}

//send current parameters to server
function sendParameters(){
    let list = getParameterList();
    if(list.length > 0) {
        httpGetCsvArrayRowCol(gotParameters, "/getModel?parameterList=" + list, 0, 10, 0, 0);
    }else{
         document.getElementById("accuracy").innerText = "please select at least one Parameter";
         document.getElementById("growthRate").innerText = "Growthrate: -";
    }
}

//deselect all parameters(usful for error catching)
function unloadParameters(){
     document.getElementById("accuracy").innerText = "Click \"Make\" to refresh parameters";
     document.getElementById("growthRate").innerText = "Growthrate: -";
    for (const key of Object.keys(parameters)) {
        document.getElementById(key + "selected").classList.remove("expandedParameter");
        document.getElementById(key + "selected").innerHTML = key;
    }
}

// handle parameter response from server
function gotParameters(result){
    unloadParameters();
    document.getElementById("accuracy").innerText = "Accuracy: " + Math.round(result[3][0] * 10000) / 100 + "%";
    for (const parameter of result[1]) {
        if (parameter !== "\r" && parameter.length > 0){
            document.getElementById(parameter + "selected").classList.add("expandedParameter");
            document.getElementById(parameter + "selected").innerHTML = "" +
                parameter +
                "<hr>" +
                "Influence: " + Math.round(result[2][result[1].indexOf(parameter)] * 10000000) / 10000000 +
                "<img src='/static/img/Black_check.svg' class='paramCheck invisible' alt='checkImage'>";
        }
    }
    predictCases(calculateGrowthRate(result), result);
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

//remove a preset from dropdown
function removePreset(){
    let x = document.getElementById("presetSelect");
    x.remove(x.selectedIndex);//OK
    delete parameterPresets[document.getElementById("presetSelect").value];
}

//add a preset to dropdown
function addPreset(){
    const option = document.createElement("option");
    const text = "Preset0" + document.getElementById("presetSelect").options.length;
    option.text = text;
    document.getElementById("presetSelect").add(option);
    document.getElementById("presetSelect").value = text;
    parameterPresets[text] = [];
    refreshPreset();
}

//TODO proper zebra effect(gradient??)
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

//manage the finalClean data file from server (only for initialisation)
let finalCleanData;
function gotFinalCleanData(struct){
    finalCleanData = struct;
    createPredictableCountriesTest(struct);
}

//calculate growthrate from server response TODO validate growthrate
function calculateGrowthRate(result){
    const predictCountry = document.getElementById("predictCountrySelect").value;
    let growthRate = 0;
    let data = {};
    for (let i = 0; i < result[1].length; i++) {
        if(result[1][i].length >= 3){
            data[result[1][i]] = result[2][i];
        }
    }
    for (const [param, value] of Object.entries(data)) {
        growthRate += value * finalCleanData[predictCountry][param];
    }
    document.getElementById("growthRate").innerText = "Growth rate: " + Math.round(growthRate * 10000) / 10000;
    return growthRate;
}

//handle changed preset from dropdown
function presetChanged(){
    loadParameterPreset(parameterPresets[document.getElementById("presetSelect").value]);
}

let predictions = [];
let predictionID = 0;
// take growthrate and add a prediction from that TODO validate prediction
function predictCases(growthRate, response){
    const predictCountry = document.getElementById("predictCountrySelect").value;
    let data = {};
    for (let t = 0; t < 100; t++) {
        data[t] = 100 * Math.pow((Math.pow(10, growthRate)), t);
    }
    addPrediction({"graph": new Graph(data, getPredictionName(predictCountry), (me, e) => me.name + ":"), "id": predictionID, "data": response});
    predictionID++;
    predictionClicked(predictionID);
}

//generate name for predictiopn from country and manage dublicates
function getPredictionName(country){
    let duplicates = 0;
    for (const p of predictions) {
        if(p.graph.name.indexOf(country) > -1){
            duplicates++;
        }
    }
    return country + (duplicates === 0 ? "" : ((duplicates < 10 ? " 0" : " ") + duplicates));
}

//add a prediction
function addPrediction(prediction){
    predictions.push(prediction);
    predictionPlotter.addGraph(prediction.graph);
    predictionPlotter.hoverGraph(prediction.graph.name);
    const predictionsList = document.getElementById("predictionList");
    predictionsList.innerHTML += getPredictionHtml(prediction);
}

function getPredictionHtml(prediction){
    return  ("<div class='noselect selected countryElement" + (predictions.length%2===0 ? " zebra" : "") + "' id='" + prediction.id + "' onclick='predictionClicked(\"" + prediction.id + "\")'>" +
                "<img src='static/img/search.svg' height='20px' width='auto' onmouseleave='predictionLeave();' onclick='predictionHovered(\"" + prediction.id + "\")' style='background-color: " + prediction.graph.color + "; margin-right: 10px;' alt='search country'>" +
                    prediction.graph.name +
                "<img style='margin-right: 6px;' height='20px' width='auto' src='/static/img/eye.svg' class='countryCheck' alt='check' onclick='predictionEyeClicked(\"" + prediction.id + "\")'>" +
            "</div>");
}

function predictionClicked(id){
    let prediction;
    for (const p of predictions) {
        if(p.id == id){ //OK
            prediction = p;
            break;
        }
    }
    if(prediction){
        document.getElementById("predictionHtml").innerHTML = getDescriptionFromPrediction(prediction);
    }
}

function predictionHovered(id){
    predictionPlotter.hoverGraph(id);
}

function predictionLeave(){

}

function predictionEyeClicked(id){
    event.stopPropagation();
    for (const prediction of predictions) {
        if(prediction.id == id){// only "==" because different type(number, string)
            setVisibleOfPrediction([prediction], !prediction.graph.visible);
        }
    }
}

function setVisibleOfPrediction(predictions, visible){
    for (const prediction of predictions) {
        prediction.graph.visible = visible;
        if(visible){
            document.getElementById(prediction.id).classList.add("selected");
        }else{
            document.getElementById(prediction.id).classList.remove("selected");
        }
    }
    predictionPlotter.draw();
}

function getDescriptionFromPrediction(prediction){
    console.log(prediction.data);
    return  "<h2>Details for \"" + prediction.graph.name + "\"</h2>" +
            "<p>To calculate this result we used static data from: <br>" + getListText(prediction.data[0]) + "</p>" +
            "<p>The following parameters have been used:<br>" + getListText(prediction.data[1]) + "</p>";
}

function removeBlanks(arr){
    let out = [];
    for (const arrElement of arr) {
        if(arrElement !== "" && arrElement !== "\r"){
            out.push(arrElement);
        }
    }
    return out;
}

function getListText(list1){
    const list = removeBlanks(list1);
    console.log(list);
    let listText = "";
    for (let i = 0; i < list.length; i++) {
        if(i < list.length - 2){
            listText += (i === 0 ? "" : ", ") + list[i];
        }else{
            listText += " and " + list[i] + ".";
        }
    }
    return listText;
}