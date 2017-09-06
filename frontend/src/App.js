import React, { Component } from "react";
import { observer } from "mobx-react";
import { plotState } from "./state";
import axios from "axios";
import "./App.css";
const serverLink = "http://127.0.0.1:5000"


class App extends React.Component {

	handleFileUpload(x) {
		console.log( x.target.value)
		let data = new FormData();
  		data.append('file', x.target.files[0]);
  		axios.post(serverLink+ '/file', data)
	      .then(response => console.log(response))
	      .catch(error => console.log(error));
	}

    render() {
        return (
   			<input type="file" onChange={this.handleFileUpload} />

        );
    }
}
  
export default App;	
