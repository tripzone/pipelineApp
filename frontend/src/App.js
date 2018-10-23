import React, { Component } from "react";
import { observer } from "mobx-react";
import { Router, Route, Link} from "react-router-dom";
import { plotState } from "./state";
import { serverLink, fileLink } from "./Setting"
import axios from "axios";
import "./App.css";


class App extends React.Component {

    render() {
        return (
        	<div className="page">
        		<div className="row">
        			<Link to="./Setting" className="btn-floating btn-large waves-effect waves-light navy menu-button"><i className="material-icons">mode_edit</i></Link>
        			<h1 className="col s12 flow-text center page-header">Technology Pipeline</h1>
        		</div>
        		<div className="row">
        			<img className="col s12" src={fileLink+"/allTech.png?"+ new Date().getTime()} />
        		</div>
                <div className="row">
                    <div className="flow-text center">Technology Pipeline For FY18</div>
                    <img className="col s12 l10 offset-l1 mar-" src={fileLink+"/90DayAll.png?"+ new Date().getTime()} />
                </div>
                <div className="row">
                     <div className="flow-text center">Service Line Deals & Key Deal Rationals</div>
                    <img className="col s12 l5  offset-l1" src={fileLink+"/SlsPlot.png?"+ new Date().getTime()} />
                    <img className="col s12 l5" src={fileLink+"/keyDealsRational.png?"+ new Date().getTime()} />   
                </div>
                <div className="row">
                    <div className="flow-text center">Close Reasons & Deal Sizes</div>
                    <img className="col s12 l5  offset-l1" src={fileLink+"/closeReasonPlot.png?"+ new Date().getTime()} />
                    <img className="col s12 l5" src={fileLink+"/dealSizePlot.png?"+ new Date().getTime()} />   
                </div>
                <div className="row">
                    <div className="flow-text center">Average Days in Each Stage & Total Deals in Age Tier</div>
                    <img className="col s12 l5  offset-l1" src={fileLink+"/averageAgePlot.png?"+ new Date().getTime()} />
                    <img className="col s12 l5" src={fileLink+"/ageTierPlot.png?"+ new Date().getTime()} />   
                </div>
        	</div>


        );
    }
}
  
export default App;	
