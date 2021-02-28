import React from 'react';
import logo from './logo.svg';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      apidata: {}
    };
  }

  componentDidMount() {
    fetch("/api/")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            apidata: result,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      )
  }

  render() {
    const {error, isLoaded, apidata} = this.state;

      return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <ApiDataTest error={error} isLoaded={isLoaded} apidata={apidata} />
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
      );
  }
}

class ApiDataTest extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.error) {
      return <p>Error: {this.props.error.message}</p>;
    } else if (!this.props.isLoaded) {
      return <p>Loading...</p>;
    }
    else {
      return <p>{JSON.stringify(this.props.apidata)}</p>
    }
  }
}

export default App;
