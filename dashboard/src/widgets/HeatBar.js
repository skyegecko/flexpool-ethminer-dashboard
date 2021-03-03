import React from 'react';

class HeatBar extends React.Component {
  render() {
    const value = this.props.value;
    const unit = this.props.unit;
    const label = this.props.label;

    return (
      <div className="HeatBar">
        <div className="label">{label}</div>
        <div className="valueAndUnit">
          <div className="value">{value}</div>
          <div className="unit">{unit}</div>
        </div>
      </div>
    );
  }
}

export default HeatBar;
