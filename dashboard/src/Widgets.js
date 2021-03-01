import React from 'react';

class BasicWidget extends React.Component {
  render() {
    return (
      <div className="BasicWidget">
        <p><strong>{this.props.name}:</strong> {this.props.value}</p>
      </div>
    );
  }
}

class HashrateDialWidget extends React.Component {
  formatHashrate(hashrate) {
    const rounded = Math.round(hashrate / 10000)
    return rounded / 100
  }

  render() {
    const hashrate = this.formatHashrate(this.props.hashrate)
    return (
      <div className="HashrateDialWidget">
        <div className="dial">
        </div>
        <div className="hashrate">
          <strong>{hashrate}</strong><br />MH/s
        </div>
        <div className="subtitle">
          Hashrate
        </div>
      </div>
    );
  }
}

export {BasicWidget, HashrateDialWidget};
