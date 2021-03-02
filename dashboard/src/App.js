import React from 'react';
import {TopBarWidget, HashrateDialWidget} from './Widgets.js';
import './App.css';

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
        <div className="Dashboard">
          <TopBarWidget
            worker={this.props.apidata.connection.worker}
            server={this.props.apidata.connection.server}
            port={this.props.apidata.connection.port}
            uptime={this.props.apidata.host.runtime_s}
          />
          <DashboardBody apidata={this.props.apidata} />
        </div>
      );
    }
  }
}

class DashboardBody extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="DashboardBody">
        <HashrateDialWidget
          hashrate={this.props.apidata.mining.hashrate}
        />
      </div>
    );
  }
}

export default App;
