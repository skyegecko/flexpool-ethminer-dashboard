import humanizeDuration from 'humanize-duration';
import React from 'react';

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

export default TopBarWidget;
