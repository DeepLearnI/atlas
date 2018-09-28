import React, { Component } from "react";
import ReactTable from "react-table";
import 'react-table/react-table.css'
import './App.css';
let columns = require('./columns');

class Completed extends Component {

  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      result: []
    };
  }

  componentDidMount() {
    fetch("http://localhost:37722/api/v1/projects/asdf/jobs/completed")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            result: result,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  render() {
    const { error, isLoaded, result } = this.state;
    var completedJobs;
    completedJobs = result.completed_jobs;

    const completed_columns = [{
      Header: 'Start Time',
      accessor: 'start_time'
    }, {
      Header: 'Status',
      accessor: 'status'
    }, {
      Header: 'JobId',
      accessor: 'job_id'
    }, {
      Header: 'User',
      accessor: 'user'
    }
  ]

  data.completed_jobs.forEach(function(x){
    var obj = x.input_params;
  
    var groupBy = obj.reduce((acc, curr) => {
        if(!acc[curr.name]) acc[curr.name] = [];
        acc[curr.name].push(curr);
        return acc;
      },{});
    
    Object.keys(groupBy).map(function(key, indexTwo) {
          if (groupBy[key].length > 1){
              groupBy[key].map(function(x, index){
                  x.name = x.name + (index + 1)
              })
          }
      });
  
    return groupBy
  
  })



    if (result.completed_jobs && result.completed_jobs[0]) {
      var inputs;
      inputs = completedJobs[0].input_params
      inputs.map(function(x) {
        var obj = {}
        obj['Header'] = x.name
        obj['Header'] = 'name'
        completed_columns.push(obj)
      })

    }

    if (error && result[0]) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {  
      return (
        <div>
            <h2>Completed Jobs</h2>
            <h3 className="project-name">Project name: {result.name}</h3>
            <h3 className="project-source">Source: not known</h3>
            <ReactTable data={completedJobs} columns={completed_columns} />
        </div>
      );
    }
  }
}

export default Completed;