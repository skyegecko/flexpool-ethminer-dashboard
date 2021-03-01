import React from 'react';
import {BasicWidget, HashrateDialWidget} from './Widgets.js';
import logo from './logo.svg';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      apidata: {}
    };

    this.reloadData = this.reloadData.bind(this);
  }

  componentWillMount() {
    this.reloadData();

    //setInterval(this.reloadData, 5000);
  }

  reloadData() {
    fetch("/api/")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            apidata: result,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      )
  }

  render() {
    const {error, isLoaded, apidata} = this.state;

    return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <Dashboard error={error} isLoaded={isLoaded} apidata={apidata} />
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
    );
  }
}

class Dashboard extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.error) {
      return <div>Error: {this.props.error.message}</div>;
    } else if (!this.props.isLoaded) {
      return <div>Loading...</div>;
    }
    else {
      return (
        <div>
          <HashrateDialWidget
            hashrate={this.props.apidata.mining.hashrate}
          />
        </div>
      );
    }
  }
}

export default App;
