import './App.css';
import React, {Component} from 'react';

import axios from 'axios';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      errorMsg: '',
      numParents: 3,
      numBlocks: 4,
    };
  }

  onFileChange = fileName => {
    return event => {
      this.setState({ [fileName]: event.target.files[0] });
    };
  };

  handleBlockChange = event => this.setState({numBlocks: event.target.value})

  getFileText = async file => {
    return new Promise((resolve,  reject) => {
      let reader = new FileReader();

      reader.onload = () => {
        resolve(reader.result);
      };

      reader.onerror = reject;

      reader.readAsText(file);
    });
  };
    

  onRunStart = async () => {
    let parentsPromise = this.getFileText(this.state.parentsFile);
    let pdbPromise = this.getFileText(this.state.pdbFile);
    let [parentsText, pdbText] = await Promise.all([
        parentsPromise.catch(error => {this.setState({errorMsg: 'Add a parents file.'})}),
        pdbPromise.catch(error => {this.setState({errorMsg: 'Add a pdb file.'})}),
    ]);
    let numBlocks = this.state.numBlocks;

    // placeholders for http call
    console.log("Sending these things:");
    console.log(parentsText);
    console.log(pdbText);
    console.log(numBlocks);

    let run_params = {parentsText, pdbText, numBlocks};
    console.log(run_params);

    axios.post("https://zuog7xflce.execute-api.us-east-1.amazonaws.com/api", run_params)
      .then(response => {
        console.log(response);
        console.log(response.data);
      });
  };

  render() {

    return (
      <div className="App">
        <div>
          <h3> Upload parent alignment FASTA: </h3>
          <input type="file" onChange={this.onFileChange("parentsFile")} />
        </div>

        <div>
          <h3> Upload PDB file: </h3>
          <input type="file" onChange={this.onFileChange("pdbFile")} />
        </div>

        <div>
          <h3> Number of blocks: </h3>
          <input id="numBlocks" type="number" value={this.state.numBlocks} onChange={this.handleBlockChange} min="2" max="8"/>
        </div>

        <button onClick={this.onRunStart}>
          Upload
        </button>

        {this.state.errorMsg && <h1> {'Error: ' + this.state.errorMsg} </h1> }
      </div>
    );
  }
}

export default App;
