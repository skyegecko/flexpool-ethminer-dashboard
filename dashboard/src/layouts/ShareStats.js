import React from 'react';
import ShareStatLine from '../widgets/ShareStatLine.js';

class ShareStats extends React.Component {
  render() {
    const {found, rejected, failed} = this.props.shares;
    const timeSince = this.props.shares.time_since_last + 's';

    return (
      <div className="ShareStats">
        <ShareStatLine label="Found" value={found} />
        <ShareStatLine label="Rejected" value={rejected} />
        <ShareStatLine label="Failed" value={failed} />
        <ShareStatLine label="Time since last" value={timeSince} />
      </div>
    );
  }
}

export default ShareStats;
