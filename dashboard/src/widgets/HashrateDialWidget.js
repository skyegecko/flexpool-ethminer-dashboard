import React from 'react';

class HashrateDialWidget extends React.Component {
  formatHashrate(hashrate) {
    return (hashrate / 1000000).toPrecision(3);
  }

  render() {
    const hashrate = this.formatHashrate(this.props.hashrate)
    return (
      <div className="HashrateDialWidget">
        <div className="dial">
        </div>
        <div className="hashratetext">
          {hashrate}
        </div>
        <div className="hashrateunits">MH/s
        </div>
      </div>
    );
  }
}

export default HashrateDialWidget;
