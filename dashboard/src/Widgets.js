import humanizeDuration from 'humanize-duration';
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

class TopBarWidget extends React.Component {
  constructor(props) {
    super(props);

    this.humanizeUptime = humanizeDuration.humanizer({
      largest: 3,
      units: ["d", "h", "m", "s"],
      round: true,
      delimiter: "",
      spacer: "",
      language: "shortEn",
      languages: {
        shortEn: {
          y: () => "y",
          mo: () => "mo",
          w: () => "w",
          d: () => "d",
          h: () => "h",
          m: () => "m",
          s: () => "s",
          ms: () => "ms",
        },
      },
    });
  }
  prettifyUptime(uptime) {
    return humanizeDuration(
      uptime * 1000, {
        largest: 3,
        units: ["d", "h", "m", "s"],
        round: true,
        delimiter: "",
        spacer: "",
      }
    );
  }

  render() {
    const worker = this.props.worker;
    const server = this.props.server;
    const port = this.props.port;
    const uptimeStr = this.humanizeUptime(this.props.uptime * 1000);

    return (
      <div className="TopBarWidget">
        <div className="worker">{worker}</div>
        <div className="server">{server}:{port}</div>
        <div className="uptime">Uptime: {uptimeStr}</div>
      </div>
    );
  }
}

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

export {BasicWidget, HashrateDialWidget, TopBarWidget};
