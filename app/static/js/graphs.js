"use strict";

class Graph{
    constructor(values, name){
        this.values = values;
        this.color = getRandomColor();
        this.visible = true;
        this.hovered = false;
        this.name = name;
    }
}

class Axis{
    constructor(name, stepNames, calculate, thickness){
        this.name = name;
        this.toolTip = "Tooltip: toDo";
        this.stepNames = stepNames;
        this.thickness = thickness;
        this.calculate = calculate;
    }
}

/**to be plotted:
 *  new plotter(canvas),
 *  set data, xAxis
 *  updateGraphsByBata()
 *  draw();
 **/
class Plotter{
    constructor(canvas){
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");
        this.data = null;
        this.graphs = [];
        this.valueFilter = e => isNumeric(e);
        this.keyFilter = e => true;
        this.xAxis = new Axis("Date", null, e => e, 20);
        this.yAxis = new Axis("Infectes", null, e => e, 60);
        this.transitionGraphs = null;
        this.keys = [];
        this.minMax = {
            'minX': 0,
            'minY': 0,
            'maxX': 0,
            'maxY': 0
        };
        this.newAnimation = true;
        this.progress
    }

    hoverGraph(name){
        let found = false;
        for (const graph of this.graphs) {
            graph.hovered = false;
            if(graph.name == name && !found){
                graph.hovered = true;
                this.focusOnGraph(graph);
                found = true;
            }
        }
        if(!found){
            this.updateMaxValues();
        }
    }

    setVisibleOfGraph(name, visible, draw){
        for (const graph of this.graphs) {
            if(graph.name == name){
                graph.visible = visible;
                if(draw && graph.visible){
                    this.focusOnGraph(graph);
                }else{
                    this.draw();
                }
            }
        }
    }

    update(){
        this.updateGraphsByData();
    }

    setData(data){
        this.data = data;
        this.updateGraphsByData();
    }

    setValueFilter(valueFilter){
        this.valueFilter = valueFilter;
        this.updateMaxValues();
    }

    setKeyFilter(keyFilter){
        this.keyFilter = keyFilter;
        this.updateKeys();
    }

    updateGraphsByData(){
        this.graphs = [];
        for (const [key, val] of Object.entries(this.data)) {
            this.graphs.push(new Graph(val, key));
        }
        this.updateKeys();
    }

    updateMaxValues(){
        let maxX = 0;
        let minX = 0;
        for (const graph of this.graphs) {
            if(!graph.visible){
                continue;
            }
            let max = 0;
            for (const [key, val] of Object.entries(graph.values)) {
                if(val != ""){
                    max++;
                }
            }
            maxX = Math.max(max, maxX);
        }
        let maxY = 0;
        let minY = -100;
        for (const graph of this.graphs) {
             if(!graph.visible){
                continue;
            }
            for (const value of Object.values(graph.values)) {
                if(this.valueFilter(value)){
                    maxY = Math.max(maxY, value);
                    minY = Math.min(minY, value);
                }
            }
        }
        this.changeMaxValues(minX, maxX, minY, maxY);
    }

    focusOnGraph(graph){
        if(!graph.visible){
            return;
        }
        let maxX = 0;
        let minX = 0;
        for (const [key, val] of Object.entries(graph.values)) {
            if(val != ""){
                maxX++;
            }
        }
        let maxY = 0;
        let minY= -10000;
        for (const value of Object.values(graph.values)) {
            if(this.valueFilter(value)){
                maxY = Math.max(maxY, value);
                minY = Math.min(minY, value);
            }
        }
        this.changeMaxValues(minX, maxX * 1.2, minY, maxY * 1.2);
    }

    updateKeys(){
        this.keys = [];
        for (const graph of this.graphs) {
            for (const [key, val] of Object.entries(graph.values)) {
                if(this.keys.indexOf(key) == -1 && this.keyFilter(key)){//keyFilter
                    this.keys.push(key);
                }
            }
        }
        this.xAxis.stepNames = this.keys;
        this.updateMaxValues();
    }

    changeMaxValues(minX, maxX, minY, maxY){
        this.animation(0, this.minMax, this.minMax, {'minX': minX, 'minY': minY, 'maxX': maxX, 'maxY': maxY});
    }

    animation(progress, changeOn, from, to){
        progress++;
        if(progress < 15 && (this.newAnimation)){
            for (const [key, val] of Object.entries(changeOn)) {
                changeOn[key] = from[key] + (to[key] - from[key]) * (progress / 15);
            }
            this.draw();
            requestAnimationFrame(() => this.animation(progress, changeOn, from, to));
        }else{
            //console.log("minY: " + changeOn.minY + ", maxY: " + changeOn.maxY);
        }
    }

    getlocationOfValue(value, xIteration){
        return{x: (this.yAxis.thickness + (xIteration / (this.minMax.maxX - this.minMax.minX)) * (this.canvas.width - this.yAxis.thickness)), y: (this.canvas.height - this.xAxis.thickness) - ((value / (this.minMax.maxY)) * (this.canvas.height - this.xAxis.thickness))};
    }

    draw(){
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.beginPath();
        for (let i = 0; i < this.minMax.maxY - 10; i += Math.max(1, Math.floor(this.minMax.maxY / 7))) {
            let point = this.getlocationOfValue(i, 0);
            this.ctx.moveTo(this.yAxis.thickness, point.y);
            this.ctx.lineTo(this.canvas.width, point.y);
            this.ctx.fillText(i + "", 1, point.y);
        }
        this.ctx.strokeStyle = "gray";
        this.ctx.stroke();
        let hovered;
        for (const graph of this.graphs) {
            if(graph.visible){
                this.ctx.strokeStyle = graph.color;
                if(graph.hovered){
                    hovered = graph;
                }else{
                    this.ctx.lineWidth = 1;
                }
                this.ctx.beginPath();
                let x = 0;
                for (const key of this.keys) {
                    if(this.valueFilter(graph.values[key])){
                        let loc = this.getlocationOfValue(graph.values[key], x);
                        this.ctx.lineTo(loc.x , loc.y);
                    }
                    x++;
                }
                this.ctx.stroke();
            }
        }
        if(hovered){
            this.ctx.beginPath();
            this.ctx.strokeStyle = hovered.color;
            this.ctx.lineWidth = 6;
            let x = 0;
            for (const key of this.keys) {
                if(this.valueFilter(hovered.values[key])){
                    let loc = this.getlocationOfValue(hovered.values[key], x);
                    this.ctx.lineTo(loc.x , loc.y);
                }
                x++;
            }
            this.ctx.stroke();
        }
        this.ctx.beginPath();
        this.ctx.moveTo(this.yAxis.thickness, this.canvas.height - this.xAxis.thickness);
        this.ctx.lineTo(this.canvas.width, this.canvas.height - this.xAxis.thickness);
        this.ctx.moveTo(this.yAxis.thickness, 0);
        this.ctx.lineTo(this.yAxis.thickness, this.canvas.height - this.xAxis.thickness);
        this.ctx.strokeStyle = "black";
        this.ctx.lineWidth = 2;
        
        this.ctx.font =  "15px Arial";
        for (let i = this.minMax.minX; i < this.minMax.maxX; i += Math.max(1, Math.round(this.minMax.maxX / 4))) {
            let point = this.getlocationOfValue(0, i);
            this.ctx.fillText(i + "", point.x, this.canvas.height - 1);
        }
        this.ctx.strokeStyle = "gray";
        this.ctx.stroke();
    }
}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(2 + Math.random() * 7)];
    }
    return color;
}

function isNumeric(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}