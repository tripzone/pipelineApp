import React, { Component } from "react";
import { observer } from "mobx-react";
import { Router, Route, Link} from "react-router-dom";
// import { plotState } from "./state";
import axios from "axios";
import "./App.css";
export const serverLink = "http://localhost:5001"

class Setting extends React.Component {

	constructor(props) {
		super(props);
		this.state = {file: new FormData(), thisPeriodYear: "2018", thisPeriodMonth:"8"};
		this.handleSubmit = this.handleSubmit.bind(this);
	}
	handleFileUpload(e,  stateFile) {
		let data = new FormData();
  		stateFile.append('file', e.target.files[0]);
	}

	handleSubmit() {
		axios.post(serverLink+ '/file', this.state.file, {
		    headers: { thisPeriodYear: this.state.thisPeriodYear, thisPeriodMonth: this.state.thisPeriodMonth }
		})
	      .then(response => 
	      	this.props.history.push('/load')
	      )
	      .catch(error => console.log(error));
	}

    render() {
        return (
        	<div className="page">
    			<div className="row">

				</div>
        		<div className="row ">
        			<div className="center offset-s1 offset-l3 offset-m2 col s10 m8 l6 teal lighten-5">
        				<div className="flow-text">
							CRM Extract
						</div>
							<div className="file-field input-field ">
							  <div className="btn">
							    <span>File</span>
							    <input type="file" onChange={(e) => this.handleFileUpload(e, this.state.file)} />
							  </div>
							  <div className="file-path-wrapper">
							    <input className="file-path validate" type="text" />
							  </div>
							</div>
        			</div>
        	   	</div>
   				<div className="row">
   					<div className="center">
   						<button className="waves-effect waves-light btn-large" onClick={e => this.handleSubmit(this.state.file)} >upload</button>
   					</div>
   				</div>
   				*Line up Date

        	</div>


        );
    }
}
  
export default Setting;	
