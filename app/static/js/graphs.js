"use strict";

class Graph{
    constructor(values, name, toolTip){
        this.values = values;
        this.toolTip = toolTip;
        this.color = getRandomColor();
        this.visible = true;
        this.hovered = false;
        this.name = name;
    }
}

class Axis{
    constructor(name, stepNames, multiplicator, thickness, toolTip){
        this.name = name;
        this.toolTip = toolTip;
        this.thickness = thickness;
        this.multiplicator = multiplicator;
    }
}

/**to be plotted:
 *  new plotter(canvas),
 *  set data, xAxis
 *  updateGraphsByBata()
 *  draw();
 **/
class Plotter{
    constructor(canvas, xName, yName, xToolTip, yToolTip){
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");
        this.canvas.addEventListener('mousemove', e => this.updateOnMouse(e));
        this.canvas.addEventListener('mouseleave', e => this.mouseInside = false);
        this.canvas.addEventListener('mouseenter', e => this.mouseInside = true);
        this.canvas.addEventListener('mouseup', e => {
            this.updateMaxValuesOnGraphs([this.hoveredGraph]);
        });
        this.mouseX = 0;
        this.mouseY = 0;
        this.toolTipWidth = 250;
        this.toolTipHeight = 75;
        this.mouseInside = false;
        this.data = null;
        this.graphs = [];
        this.hoveredGraph = {};
        this.valueFilter = e => isNumeric(e);
        this.keyFilter = e => true;
        this.logaRythmus = false;
        this.xAxis = new Axis(xName, "", 1, 20, xToolTip);
        this.yAxis = new Axis(yName, "", 10, 60, yToolTip);
        this.keys = [];
        this.minMax = {
            'minX': 0,
            'minY': 0,
            'maxX': 0,
            'maxY': 0
        };
        this.newAnimation = true;
    }

    hoverGraph(name){
        let found = false;
        for (const graph of this.graphs) {
            if(!graph.visible){
                continue;
            }
            graph.hovered = false;
            if(graph.name === name && !found){
                this.removeHovered();
                graph.hovered = true;
                this.updateMaxValuesOnGraphs([graph]);
                found = true;
            }
        }
    }

    setVisibleOfGraph(name, visible, draw){
        for (const graph of this.graphs) {
            if(graph.name === name){
                graph.visible = visible;
                if(draw && graph.visible){
                    this.updateMaxValuesOnGraphs([graph]);
                }else{
                    this.draw();
                }
            }
        }
    }

    update(){
        this.updateGraphsByData();
    }

    setData(data, toolTip){
        this.data = data;
        this.updateGraphsByData(toolTip);
    }

    setValueFilter(valueFilter){
        this.valueFilter = valueFilter;
        this.updateMaxValuesOnGraphs(this.graphs);
    }

    setKeyFilter(keyFilter){
        this.keyFilter = keyFilter;
        this.updateKeys();
    }

    updateGraphsByData(toolTip){
        this.graphs = [];
        for (const [key, val] of Object.entries(this.data)) {
            this.graphs.push(new Graph(val, key, toolTip));
        }
        this.updateKeys();
    }

    updateMaxValuesOnGraphs(graphs){
        let maxX = -100000;
        let minX = 100000;
        for (const graph of graphs) {
            if(!graph.visible){
                continue;
            }
            let max = 0;
            for (const [key, val] of Object.entries(graph.values)) {
                if(val !== ""){
                    max++;
                    if(isNumeric(key) && this.keyFilter(key)){
                        minX = Math.min(minX, parseInt(key));
                    }
                }
            }
            maxX = Math.max(max, maxX);
        }
        let maxY = -100000;
        let minY = 100000;
        for (const graph of graphs) {
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
        this.changeMaxValues(minX, maxX + 2, minY, maxY * 1.2);
    }

    updateKeys(){
        this.keys = [];
        for (const graph of this.graphs) {
            for (const [key, val] of Object.entries(graph.values)) {
                if(this.keys.indexOf(key) === -1 && this.keyFilter(key)){//keyFilter
                    this.keys.push(key);
                }
            }
        }
        this.xAxis.stepNames = this.keys;
        this.updateMaxValuesOnGraphs(this.graphs);
    }

    changeMaxValues(minX, maxX, minY, maxY){
        this.animation(0, this.minMax, this.minMax, {'minX': Math.round(minX), 'minY': Math.round(minY), 'maxX': Math.round(maxX), 'maxY': Math.round(maxY)});
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
            for (const [key, val] of Object.entries(changeOn)) {
                changeOn[key] = Math.round(val);
            }
            this.draw();
        }
    }

    getBaseLog(x, y) {
        return Math.log(y) / Math.log(x);
    }

    getXIterationFromX(x){
        return this.minMax.minX + (((x - this.yAxis.thickness) / (this.canvas.width - this.yAxis.thickness)) * (this.minMax.maxX - this.minMax.minX));
    }

    getLocationOfValue(value, xIteration) {
        if(this.logaRythmus){
            return{x: (this.yAxis.thickness + ((xIteration - this.minMax.minX) / (this.minMax.maxX - this.minMax.minX)) * (this.canvas.width - this.yAxis.thickness)), y: (this.canvas.height - this.xAxis.thickness) - (this.getBaseLog(this.yAxis.multiplicator, (value - this.minMax.minY)) / this.getBaseLog(this.yAxis.multiplicator, (this.minMax.maxY - this.minMax.minY)) * (this.canvas.height - this.xAxis.thickness))};
        }else{
            return{x: (this.yAxis.thickness + ((xIteration - this.minMax.minX) / (this.minMax.maxX - this.minMax.minX)) * (this.canvas.width - this.yAxis.thickness)), y: (this.canvas.height - this.xAxis.thickness) - ((value - this.minMax.minY) / (this.minMax.maxY - this.minMax.minY) * (this.canvas.height - this.xAxis.thickness))};
        }
    }

    updateOnMouse(e){
        this.mouseX = e.clientX - this.canvas.getBoundingClientRect().left;
        this.mouseY = e.clientY - this.canvas.getBoundingClientRect().top;
        this.draw();
    }

    removeHovered(){
        for (const graph of this.graphs) {
            graph.hovered = false;
        }
    }

    grayAllOutExeptOf(graph){
        for (const graph1 of this.graphs) {
            if(graph1 != graph){
                graph1.color = "";
            }
        }
    }

    draw(){
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.fillStyle = "black";
        let hover = false;
        let xIteration;
        if(this.mouseInside && isNumeric(this.mouseX) && isNumeric(this.mouseY)) {
            let minDistance = {};
            minDistance["distance"] = this.canvas.height;
            xIteration = Math.round(this.getXIterationFromX(this.mouseX));
            let point;
            if (this.mouseInside) {
                for (const graph of this.graphs) {
                    if(!graph.visible){
                        continue;
                    }
                    if (isNumeric(graph.values[xIteration]) && this.valueFilter(graph.values[xIteration]) && xIteration >= this.minMax.minX) {
                        point = this.getLocationOfValue(graph.values[xIteration], xIteration);
                        let dis = distance(this.mouseX, this.mouseY, point.x, point.y);
                        if (dis < minDistance["distance"]) {
                            minDistance["graph"] = graph;
                            minDistance["distance"] = dis;
                        }
                    }
                }
            }
            if(minDistance["graph"] != null) {
                this.removeHovered();
                minDistance["graph"].hovered = true;
                hover = true;
                this.hoveredGraph = minDistance["graph"];
            }
        }
        this.ctx.beginPath();
        let count = 1;
        // y axis names and horizontal lines
        //TODO more appealing numbers :/
        for (let i = this.logaRythmus ? 100 : parseInt(this.minMax.minY); i < this.minMax.maxY; this.logaRythmus ? i = Math.pow(this.yAxis.multiplicator, count) : i += Math.max(5, Math.floor((this.minMax.maxY - this.minMax.minY) / 100) * 10)) {
            let point = this.getLocationOfValue(i, 0);
            this.ctx.moveTo(this.yAxis.thickness, point.y);
            this.ctx.lineTo(this.canvas.width, point.y);
            this.ctx.fillText(i + "", 1, point.y);
            count++;
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
                let x = this.minMax.minX;
                for (const key of this.keys) {
                    if(this.valueFilter(graph.values[key])){
                        let loc = this.getLocationOfValue(graph.values[key], x);
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
            let x = this.minMax.minX;
            for (const key of this.keys) {
                if(this.valueFilter(hovered.values[key])){
                    let loc = this.getLocationOfValue(hovered.values[key], x);
                    this.ctx.lineTo(loc.x , loc.y);
                }
                x++;
            }
            this.ctx.stroke();
        }
        this.ctx.beginPath();
        this.ctx.moveTo(this.yAxis.thickness, this.canvas.height - this.xAxis.thickness);
        this.ctx.lineTo(this.canvas.width - 7, this.canvas.height - this.xAxis.thickness);
        this.ctx.moveTo(this.yAxis.thickness, 7);
        this.ctx.lineTo(this.yAxis.thickness, this.canvas.height - this.xAxis.thickness);
        //x Arrow
        this.ctx.moveTo(this.canvas.width - 10, this.canvas.height - this.xAxis.thickness - 7);
        this.ctx.lineTo(this.canvas.width - 1, this.canvas.height - this.xAxis.thickness);
        this.ctx.lineTo(this.canvas.width - 10, this.canvas.height - this.xAxis.thickness + 7);
        //y Arrow
        this.ctx.moveTo(this.yAxis.thickness - 7, 10);
        this.ctx.lineTo(this.yAxis.thickness, 1);
        this.ctx.lineTo(this.yAxis.thickness + 7, 10);
        this.ctx.lineCap = "butt";
        this.ctx.fillStyle = "black";
        this.ctx.lineWidth = 2;

        //y Axis values
        this.ctx.font =  "15px Arial";
        for (let i = this.minMax.minX; i < this.minMax.maxX; i += Math.max(1, Math.round(this.minMax.maxX / 4))) {
            let point = this.getLocationOfValue(0, i);
            this.ctx.fillText(Math.round(i) + "", point.x - 1, this.canvas.height - 1);
        }
        this.ctx.strokeStyle = "black";
        this.ctx.stroke();
        this.ctx.fillText(this.xAxis.name, this.canvas.width - (this.xAxis.name.length * 7 + 20), this.canvas.height - this.xAxis.thickness - 5);
        this.ctx.fillText(this.yAxis.name, this.yAxis.thickness + 10, 20);
        if(hover){
            const point = this.getLocationOfValue(this.hoveredGraph.values[xIteration], xIteration);
            const x = Math.min(point.x, this.canvas.width - this.toolTipWidth);
            const y = Math.min(point.y, this.canvas.height - this.toolTipHeight - this.xAxis.thickness);
            this.ctx.fillStyle = this.hoveredGraph.color;

            this.ctx.beginPath();
            this.ctx.arc(point.x, point.y, 8,0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.strokeStyle = "gray";
            this.ctx.beginPath();
            this.ctx.moveTo(this.mouseX , 0);
            this.ctx.lineTo(this.mouseX, this.canvas.height - this.xAxis.thickness);
            this.ctx.rect(x,y,this.toolTipWidth, this.toolTipHeight);
            this.ctx.stroke();
            this.ctx.fillStyle = "rgba(200,200,200,0.8)";
            this.ctx.fillRect(x, y, this.toolTipWidth, this.toolTipHeight);
            this.ctx.fillStyle = "black";
            this.ctx.fillText(this.hoveredGraph.toolTip(this.hoveredGraph, xIteration), x + 10, y+ 15);
            this.ctx.fillText(this.xAxis.toolTip(xIteration), x + 10, y + 40);
            this.ctx.fillText(this.yAxis.toolTip(this.hoveredGraph.values[xIteration]), x + 10, y + 65);
            this.ctx.strokeStyle = "black";
        }
    }
}

function distance(x1, y1, x2, y2){
    const x = x1 - x2;
    const y = y1 - y2;
    return Math.sqrt(x * x + y * y);
}

function getRandomColor() {
    let letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(2 + Math.random() * 10)];
    }
    return color;
}

function isNumeric(n) {
    if(typeof n == "string"){
        for (let i = 0; i < n.length; i++) {
            if(isNaN(parseFloat(n[i]))){
                return false;
            }
        }
    }
    return !isNaN(parseFloat(n)) && isFinite(n);
}