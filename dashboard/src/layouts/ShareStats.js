import React from 'react';
import ShareStatLine from '../widgets/ShareStatLine.js';
import ShareSinceLastLine from '../widgets/ShareSinceLastLine.js';

class ShareStats extends React.Component {
  render() {
    const {difficulty, hashrate} = this.props.mining;
    const {found, rejected, failed} = this.props.mining.shares;
    const timeSince = this.props.mining.shares.time_since_last;

    return (
      <div className="ShareStats">
        <ShareStatLine label="Found" value={found} />
        <ShareStatLine label="Rejected" value={rejected} />
        <ShareStatLine label="Failed" value={failed} />
        <ShareSinceLastLine
          label="Time since last"
          value={timeSince}
          difficulty={difficulty}
          hashrate={hashrate}
        />
      </div>
    );
  }
}

export default ShareStats;
