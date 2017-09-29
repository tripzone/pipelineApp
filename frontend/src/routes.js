import React from "react";
import { Router, Route, Link } from "react-router-dom";
import App from "./App";
import PlotLoad from "./PlotLoad";
import Setting from "./Setting";
import { createBrowserHistory } from 'history';


const Routes = () =>
	<Router history={createBrowserHistory()}>
		<div>
			<Route exact path="/" component={App} />
			<Route path="/setting" component={Setting} />
			<Route path="/load" component={PlotLoad} />
		</div>
	</Router>
export default Routes;
