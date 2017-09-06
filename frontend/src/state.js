import { observable, action } from "mobx";

class plot {
	@observable loaded = false;
	@observable type = "";
	@observable category = "";

	constructor(type, category) {
		this.loaded = false;
		this.error = false;
		this.type = type;
		this.category = category;
	}
}

export let plotState = observable({
	"loaded" : false,
	"plots" : []
});
plotState.init = function(plotTypes) {
	this.loaded = true;
	plotTypes.forEach(x=>{
		this.plots.push(new plot(x.type, x.category))
	})
};
plotState.loadPlot = function(type){
	this.plots[this.plots.findIndex(x=>x.type ==type)].loaded = true;
}
plotState.loadError = function(type){
	this.plots[this.plots.findIndex(x=>x.type ==type)].error = true;
}
