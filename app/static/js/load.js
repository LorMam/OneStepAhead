"use strict";

function httpGetCsvStruct(done, url){
    httpGet(e => done(csvToJsonHeaderAndFirstCol(e)), url);
}

function httpGetCsvArray(done, url){
    httpGet(e => done(csvToArray(e)), url);
}

function httpGet(done, url) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                done(xhr.responseText);
            } else {
                console.error("error: " + xhr.statusText);
            }
        }
    };
    xhr.onerror = function (e) {
        console.error("error: " + xhr.statusText);
    };
    xhr.send(null);
}

function csvToJsonOnlyHeaders(csv){
    const arr = csv.split('\n');
    const jsonObj = [];
    const headers = arr[0].split(',');
    for(let row = 1; row < arr.length; row++) {
        const data = arr[row].split(',');
        for(let col = 0; col < data.length; col++) {
            if(jsonObj.hasOwnProperty(headers[col])){
                jsonObj[headers[col]].push(data[col]);
            }else{
                jsonObj[headers[col]] = [];
                jsonObj[headers[col]].push(data[col]);
            }   
        }
    }
    return jsonObj;
}

function csvToJsonHeaderAndFirstCol(csv){
    const arr = csv.split('\n');
    const jsonObj = {};
    const headers = arr[0].split(',');
    for (let i = 0; i < headers.length; i++) {
        headers[i] = filterString(headers[i]);
    }
    for(let row = 1; row < arr.length; row++) {
        const data = arr[row].split(',');
        for(let col = 1; col < data.length; col++) {
            if(jsonObj.hasOwnProperty(headers[col])){
                jsonObj[headers[col]][data[0]] = filterString(data[col]);
            }else{
                jsonObj[headers[col]] = {};
                jsonObj[headers[col]][data[0]] = filterString(data[col]);
            }
        }
    }
    return jsonObj;
}

function csvToArray(csv){
    return csv.split(',');
}

function filterString(string){
    return string.replace(/'/g, '');
}