"use strict";

function httpGetCsvStruct(done, url){
    httpGet(e => done(csvToJsonHeaderAndFirstCol(e)), url);
}

function httpGetCsvArray(done, url, rowStart, rowEnd, colStartTrim, colEndTrim){
    httpGet(e => done(csvToArray(e, rowStart, rowEnd, colStartTrim, colEndTrim)), url);
}

function httpGetCsvArrayRowCol(done, url, rowStart, rowEnd, colStartTrim, colEndTrim){
    httpGet(e => done(csvToArrayRowCol(e, rowStart, rowEnd, colStartTrim, colEndTrim)), url);
}

function httpGet(done, url) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                done(xhr.responseText);
            } else {
                console.log(url);
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

function csvToArrayRowCol(csv, rowStart, rowEnd, colStartTrim1, colEndTrim1){
    console.log(csv);
    const rows = csv.split("\n");
    const out = [];
    let colEndTrim = 0;
    let colStartTrim = 0;
    if(colStartTrim1){
        colStartTrim = colStartTrim1;
    }
     if(colEndTrim1){
        colEndTrim = colEndTrim1;
     }
     let row1 = 0;
     let col1 = 0;
     for (let i = rowStart; i < Math.min(rowEnd, rows.length); i++) {
        let data = rows[i].split(',');
        col1 = 0;
        out[row1] = [];
        for (let col = colStartTrim; col < data.length - colEndTrim; col++) {
            out[row1][col1] = data[col];
            col1++;
        }
        row1++;
    }
    return out;
}

function csvToArray(csv, rowStart, rowEnd, colStartTrim1, colEndTrim1){
    const rows = csv.split("\n");
    const out = [];
    let colEndTrim = 0;
    let colStartTrim = 0;
    if(colStartTrim1){
        colStartTrim = colStartTrim1;
    }
     if(colEndTrim1){
        colEndTrim = colEndTrim1;
    }
    let count = 0;
    for (let i = rowStart; i < Math.min(rowEnd, rows.length); i++) {
        let data = rows[i - rowStart].split(',');
        for (let col = colStartTrim; col < data.length - colEndTrim; col++) {
            out[count] = data[col];
            count++;
        }
    }
    return out;
}

function filterString(string){
    return string.replace(/'/g, '');
}