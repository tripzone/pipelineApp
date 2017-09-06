import React, { Component } from "react";
import { observer } from "mobx-react";
import { plotState } from "./state";
import "./App.css";

const serverLink = "http://127.0.0.1:5000"

async function plotIt(type) {
	return fetch(serverLink+"/makeplot", {
		method: "GET",
		headers: new Headers({
			"plot-type": type
		})
	}).then(x => {
			return x.json()
		}
		);
}

function getPlotTypes() {
	return fetch(serverLink+"/plottypes", {
		method: "GET"
	}).then(response => response.json()).catch(x=>errorPlotTypes());
}

function loadPlot(plot) {
	plotState.loadPlot(plot.type)

}

function loadError(plot) {
	console.log('loading error mang')
	plotState.loadError(plot.type)

}

function loadPlotTypes(plotTypes){
	plotState.init(plotTypes)
}

function errorPlotTypes() {
	console.warn('error ')
	plotState.errorPlotTypes()
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

		const imageSelector = (state) => {
			if (!state.loadedState) {
				return "loading.gif"
			} else if (state.loaderror) {
				return "error.png"
			} else if (state.loadedState) {
				return picLink(state.category)
			}
		} 

		return(
			<div className="row">
				<img src={imageSelector(this.props)} />
				<div>{this.props.desc}</div>
			</div>
		)		

	}

}

@observer
class App extends Component {
	componentWillMount() {
		const requests = async () => {
			const plotTypes = await getPlotTypes();
			if (plotTypes.length > 0) {loadPlotTypes(plotTypes) } else { errorPlotTypes()};
			plotTypes.forEach(async x => {
				plotIt(x.type).then(y=>{y.success ? loadPlot(x) : loadError(x)}).catch(x=> loadError(x));
			});
			return { done: "yes" };
		};

		requests()
			.then(x => console.log("all good bro", x))
			.catch(x => console.log("no good", x));
	}

	render() {

		if (!plotState.loaded) {
			return (
				<div className="row">
					{!plotState.error ? "Loading..." : "SERVER ERROR"}
				</div>

			)
		} else if (plotState.loaded) {
			return (
				<div className="loading_main">
					<div className="row">
						<div className="flow-text center">Generating Plots</div>
					</div>
					<div className="row">
						{plotState.plots.map(x=><div className="col s6 m4 l2 loading_plot center"><LoadingPlot key={x.name} loadedState={x.loaded} category={x.category} loaderror={x.error} desc={x.desc} /></div>)}
					</div>
				</div>
			);
		}

	}
}

export default App;
