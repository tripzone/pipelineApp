import { observable, action } from "mobx";

class plot {
	@observable loaded = false;
	@observable error = false;
	@observable type = "";
	@observable category = "";
	@observable desc = "";

	constructor(type, category, desc) {
		this.loaded = false;
		this.error = false;
		this.type = type;
		this.category = category;
		this.desc = desc
	}
}

export let plotState = observable({
	"loaded" : false,
	"error": false,
	"plots" : []
});
plotState.init = function(plotTypes) {
	this.loaded = true;
	plotTypes.forEach(x=>{
		this.plots.push(new plot(x.type, x.category, x.desc))
	})
};
plotState.loadPlot = function(type){
	this.plots[this.plots.findIndex(x=>x.type ==type)].loaded = true;
}
plotState.loadError = function(type){
	this.plots[this.plots.findIndex(x=>x.type ==type)].loaded = true;
	this.plots[this.plots.findIndex(x=>x.type ==type)].error = true;
}
plotState.errorPlotTypes  = function (){
	this.error = true;
}