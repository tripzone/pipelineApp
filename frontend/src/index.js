import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import registerServiceWorker from "./registerServiceWorker";
import Routes from "./routes";
import { browserHistory } from "react-router";

ReactDOM.render(<Routes />, document.getElementById("root"));
registerServiceWorker();
