import React, { Component } from "react";
import { observer } from "mobx-react";
import { Router, Route, Link} from "react-router-dom";
import { plotState } from "./state";
import axios from "axios";
import "./App.css";
const serverLink = "http://127.0.0.1:5000"


class App extends React.Component {

	constructor(props) {
		super(props);
		this.state = {file: new FormData()};
		this.handleSubmit = this.handleSubmit.bind(this);

	}
	handleFileUpload(e,  stateFile) {
		let data = new FormData();
  		stateFile.append('file', e.target.files[0]);
	}

	handleSubmit() {

		console.log('here bro')
		axios.post(serverLink+ '/file', this.state.file)
	      .then(response => 
	      	this.props.history.push('/load')
	      )
	      .catch(error => console.log(error));
	}

    render() {
        return (
        	<div>
        	   	<input type="file" onChange={(e) => this.handleFileUpload(e, this.state.file)} />
   				<button onClick={e => this.handleSubmit(this.state.file)} >upload</button>
   				<Link to="/load">Home</Link>

        	</div>


        );
    }
}
  
export default App;	
