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

function loadError(plot) {
	plotState.loadError(plot.type)

}

function loadPlotTypes(plotTypes){
	plotState.init(plotTypes)
}

class LoadingPlot extends Component {
	render() {
		const picLink = (type) =>{
			const picTypes = {
				table: 'table.png',
				pie: 'pie.png',
				area: 'area.png',
				bar: 'bar.png'
			}

			if (picTypes[type]) {
				return picTypes[type]
			} else {
				return picTypes[0]
			}
		}

		if (!this.props.loadedState) {
			return(<span>
						<img src="loading.gif" />
					</span>
			)
		} else if (this.props.loadedState ) {
			return(	<span>
						<img src={picLink(this.props.category)} />
					</span>
			)
		} 
	}

}

@observer
class App extends Component {
	componentWillMount() {
		const requests = async () => {
			const plotTypes = await getPlotTypes();
			loadPlotTypes(plotTypes)
			plotTypes.forEach(async x => {
				plotIt(x.type).then(y=>{y.success ? loadPlot(x) : loadError(x)}).catch(loadError(x));
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
				<div className="row">
					{plotState.loaded ? plotState.plots.map(x=><div className="col s6 m3 l2 loading_plot"><LoadingPlot key={x.name} loadedState={x.type} category={x.category} /></div>) : "Loading..."}
				</div>

			</div>
		);
	}
}

export default App;
