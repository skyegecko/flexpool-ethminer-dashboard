import React from 'react';

class ShareSinceLastLine extends React.Component {
  calcHighlight(timeSince, difficulty, hashrate) {
    const expectedTime = difficulty / hashrate;
    const badTime = expectedTime * 1.5;

    if (timeSince <= expectedTime) return "good";
    else if (timeSince <= badTime) return "poor";
    else return "bad";
  }
  render() {
    const label = this.props.label;
    const value = this.props.value;
    const difficulty = this.props.difficulty;
    const hashrate = this.props.hashrate;
    const highlightClass = this.calcHighlight(value, difficulty, hashrate);
    const expectedTime = difficulty / hashrate;

    return (
      <div className="ShareStatLine ShareSinceLastLine">
        {label}:
        <span className={"value " + highlightClass}>{value}</span>s
      </div>
    );
  }
}

export default ShareSinceLastLine;
