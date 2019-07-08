import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';
import HoverCell from '../JobListPage/cells/HoverCell';

class InputMetricCell extends Component {
  constructor(props) {
    super(props);
    this.toggleExpand = this.toggleExpand.bind(this);
    this.state = {
      value: this.props.value,
      isError: this.props.isError,
      cellType: this.props.cellType,
      rowNumber: this.props.rowNumber,
    };
  }

  toggleExpand(value) {
    this.setState({ expand: value });
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ value: nextProps.value });
  }

  render() {
    const {
      value, isError, cellType, rowNumber, expand,
    } = this.state;

    const pClass = CommonActions.getInputMetricCellPClass(isError, cellType);
    const divClass = CommonActions.getInputMetricCellDivClass(isError, rowNumber);

    let hover;

    if (expand) {
      hover = <HoverCell textToRender={value} />;
    }

    return (
      <div className={divClass}>
        <p
          className={pClass}
          onMouseEnter={() => this.toggleExpand(true)}
          onMouseLeave={() => this.toggleExpand(false)}
        >
          {value}
        </p>
        <div>
          {hover}
        </div>
      </div>
    );
  }
}

InputMetricCell.propTypes = {
  value: PropTypes.any,
  isError: PropTypes.bool,
  cellType: PropTypes.string,
  rowNumber: PropTypes.number,
};

InputMetricCell.defaultProps = {
  value: '',
  isError: false,
  cellType: '',
  rowNumber: 0,
};

export default InputMetricCell;
