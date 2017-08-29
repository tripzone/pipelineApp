import React, { Component } from "react";
import { observer } from "mobx-react";
import { var1, count } from "./state";
import "./App.css";

async function plotIt(type) {
	fetch("http://127.0.0.1:5000/makeplot", {
		method: "GET",
		headers: new Headers({
			"plot-type": type
		})
	}).then(x => x.json());
}

async function getPlotTypes() {
	const response = await fetch("http://127.0.0.1:5000/plottypes", {
		method: "GET"
	});
	return response.json();
}

@observer
class App extends Component {
	componentWillMount() {
		const requests = async () => {
			const plotTypes = await getPlotTypes();
			plotTypes.forEach(async x => {
				console.log(x.type);
				plotIt(x.type);
			});
			return { done: "yes" };
		};

		requests()
			.then(x => console.log("all good bro", x))
			.catch(x => console.log("no good", x));
	}

	render() {
		const oss = new var1("name", 3);
		count.inc();

		return (
			<div className="App">
				ola
				{oss.name}
				{count.id}
			</div>
		);
	}
}

export default App;
