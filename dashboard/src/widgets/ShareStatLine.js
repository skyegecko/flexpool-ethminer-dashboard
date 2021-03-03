import React from 'react';

class ShareStatLine extends React.Component {
  render() {
    const label = this.props.label;
    const value = this.props.value;

    return (
      <div className="ShareStatLine">
        <span className="label">{label}:</span>
        <span className="value">{value}</span>
      </div>
    )
  }
}

export default ShareStatLine;
