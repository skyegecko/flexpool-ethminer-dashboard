import React from 'react';
import './App.css';
import Dashboard from './layouts/Dashboard.js';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      apidata: {},
      refreshTimer: null,
    };

    this.reloadData = this.reloadData.bind(this);
  }

  componentDidMount() {
    this.reloadData();

    const refreshTimer = setInterval(this.reloadData, 5000);
    this.setState({refreshTimer: refreshTimer})
  }

  componentWillUnmount() {
    const refreshTimer = this.state.refreshTimer;
    clearInterval(refreshTimer);
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
      <Dashboard error={error} isLoaded={isLoaded} apidata={apidata} />
    </div>
    );
  }
}


export default App;
