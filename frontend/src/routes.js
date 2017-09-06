import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import App from "./App";
import PlotLoad from "./PlotLoad"

const Routes = () =>
	<Router>
		<div>
			<Route exact path="/" component={App} />
			<Route path="/load" component={PlotLoad} />
		</div>
	</Router>
export default Routes;
