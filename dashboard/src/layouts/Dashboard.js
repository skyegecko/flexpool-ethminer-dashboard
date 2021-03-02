import React from 'react';
import TopBarWidget from '../widgets/TopBarWidget.js';
import HashrateDialWidget from '../widgets/HashrateDialWidget.js';

class Dashboard extends React.Component {
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


export default Dashboard;
