import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableSectionHeader from './TableSectionHeader';
import JobColumnHeader from './JobColumnHeader';
import InputMetricCell from './InputMetricCell';
import InputMetricRow from './InputMetricRow';
import CommonActions from '../../actions/CommonActions';

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.resizeCells = this.resizeCells.bind(this);
    this.state = {
      header: this.props.header,
      hiddenInputParams: this.props.hiddenInputParams,
      allInputParams: this.props.allInputParams,
      jobs: [],
      cellWidths: new Array(5),
      isMetric: this.props.isMetric,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ allInputParams: nextProps.allInputParams, jobs: nextProps.jobs });
  }

  resizeCells(colIndex, newWidth) {
    const { cellWidths } = this.state;
    if (cellWidths[colIndex] !== newWidth) {
      cellWidths[colIndex] = newWidth;
      this.forceUpdate();
    }
  }

  render() {
    const {
      header, hiddenInputParams, allInputParams, jobs, cellWidths, isMetric,
    } = this.state;

    const inputParams = CommonActions.getInputMetricColumnHeaders(allInputParams, this.resizeCells);
    const rows = CommonActions.getInputMetricRows(jobs, cellWidths, isMetric, allInputParams);

    return (
      <div className="input-metric-container">
        <TableSectionHeader header={header} />
        <div className="input-metric-column-header-container">
          {inputParams}
          {rows}
        </div>
      </div>
    );
  }
}

InputMetric.propTypes = {
  header: PropTypes.string,
  hiddenInputParams: PropTypes.array,
  allInputParams: PropTypes.array,
  jobs: PropTypes.array,
  cellWidths: PropTypes.array,
  isMetric: PropTypes.bool,
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
  jobs: [],
  cellWidths: [],
  isMetric: false,
};


export default InputMetric;
