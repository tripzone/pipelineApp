import React, { Component } from "react";
import { observer } from "mobx-react";
import { plotState } from "./state";
import "./App.css";

async function plotIt(type) {
	return fetch("http://127.0.0.1:5000/makeplot", {
		method: "GET",
		headers: new Headers({
			"plot-type": type
		})
	}).then(x => {
			return x.json()
		}
		);
}

async function getPlotTypes() {
	const response = await fetch("http://127.0.0.1:5000/plottypes", {
		method: "GET"
	});
	return response.json();
}

function loadPlot(plot) {
	plotState.loadPlot(plot.type)

}

function loadPlotTypes(plotTypes){
	plotState.init(plotTypes)
}

@observer
class App extends Component {
	componentWillMount() {
		const requests = async () => {
			const plotTypes = await getPlotTypes();
			loadPlotTypes(plotTypes)
			plotTypes.forEach(async x => {
				plotIt(x.type).then(y=>{y.success ? loadPlot(x) : console.log('nada')});
			});
			return { done: "yes" };
		};

		requests()
			.then(x => console.log("all good bro", x))
			.catch(x => console.log("no good", x));
	}

	render() {


		return (
			<div className="App">
				ola
				{plotState.loaded ? "yup" : "nope"}
			</div>
		);
	}
}

export default App;
