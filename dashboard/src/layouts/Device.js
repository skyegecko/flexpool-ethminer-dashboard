import React from 'react';
import HeatBar from '../widgets/HeatBar.js';

class Device extends React.Component {
  render() {
    const deviceData = this.props.deviceData
    return (
      <div className="Device">
        <div className="device-name">
          {deviceData.name}
        </div>
        <div className="heatbar-box">
          <HeatBar
            label="Temp."
            unit="°C"
            value={deviceData.temp_c}
          />
          <HeatBar
            label="Power"
            unit="W"
            value={Math.round(deviceData.power_w)}
          />
        </div>
      </div>
    );
  }
}

export default Device;
