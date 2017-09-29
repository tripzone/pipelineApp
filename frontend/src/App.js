import React, { Component } from "react";
import { observer } from "mobx-react";
import { Router, Route, Link} from "react-router-dom";
import { plotState } from "./state";
// import Setting from "./Setting";
import axios from "axios";
import "./App.css";
const serverLink = "http://127.0.0.1:5000"


class App extends React.Component {

    render() {
        return (
        	<div className="page">
        		<div className="row">
        			<Link to="./Setting" className="btn-floating btn-large waves-effect waves-light green menu-button"><i className="material-icons">mode_edit</i></Link>
        			<h1 className="col s12 flow-text center page-header">Technology Pipeline</h1>
        		</div>
        		<div className="row">
        			<img src="/Users/kzahir/dev/deloitte/pipelineApp/app/output/allTech.png" />
        		</div>
        	</div>


        );
    }
}
  
export default App;	
