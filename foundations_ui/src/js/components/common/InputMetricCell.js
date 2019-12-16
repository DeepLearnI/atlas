import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';
import HoverCell from '../JobListPage/cells/HoverCell';
import Tag from './Tag';

const maxLength = 2;

class InputMetricCell extends Component {
  constructor(props) {
    super(props);
    this.toggleExpand = this.toggleExpand.bind(this);
    this.onClick3Dots = this.onClick3Dots.bind(this);
    this.state = {
      value: this.props.value,
      isError: this.props.isError,
      cellType: this.props.cellType,
      rowNumber: this.props.rowNumber,
      hoverable: this.props.hoverable,
      jobID: this.props.jobID,
    };
  }

  toggleExpand(value) {
    this.setState({ expand: value });
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      value: nextProps.value,
      cellType: nextProps.cellType,
      rowNumber: nextProps.rowNumber,
      isError: nextProps.isError,
      hoverable: nextProps.hoverable,
      jobID: nextProps.jobID,
    });
  }

  getDisplayText(value) {
    if (value.key !== undefined) { // we know its a react element
      if (value.key === null) { // the react element does not have a value set to display
        return '';
      }
      return value.key;
    }
    return value; // typical content
  }

  isTagContentOverMaxLength(displayText) {
    return displayText.length > maxLength;
  }

  isContentOverMaxLength(displayText) {
    const maxCellCharacterLength = 24;
    return displayText.toString().length > maxCellCharacterLength || displayText.length > maxCellCharacterLength;
  }

  onClick3Dots() {
    const { onClickOpenModalJobDetails, jobID } = this.props;
    onClickOpenModalJobDetails(jobID);
  }

  render() {
    const {
      value, isError, cellType, rowNumber, expand, hoverable, jobID,

    } = this.state;
    const { columnHeader } = this.props;

    const pClass = CommonActions.getInputMetricCellPClass(isError, cellType);
    const divClass = CommonActions.getInputMetricCellDivClass(isError, rowNumber, jobID);
    let hover;

    let finalValue = value;
    let expandedValue = value;
    const shouldCheckExpand = expand;
    const dataClass = '';
    if (pClass.includes('tag') && value !== '') {
      finalValue = [];
      let index = 0;
      if (Array.isArray(value)) {
        value.forEach(tag => {
          if (index === maxLength) {
            expandedValue = Array.from(finalValue);
            expandedValue.push(<Tag key={tag} value={tag} />);
            finalValue.push(<p onClick={this.onClick3Dots} onKeyDown={() => {}}>...</p>);
          } else if (index < maxLength) {
            finalValue.push(<Tag key={tag} value={tag} />);
          } else {
            expandedValue.push(<Tag key={tag} value={tag} />);
          }
          index += 1;
        });
      } else {
        Object.keys(value).forEach(tag => {
          if (index === maxLength) {
            expandedValue = Array.from(finalValue);
            expandedValue.push(<Tag key={tag} value={tag} />);
            finalValue.push(<p onClick={this.onClick3Dots} onKeyDown={() => {}}>...</p>);
          } else if (index < maxLength) {
            finalValue.push(<Tag key={tag} value={tag} />);
          } else {
            expandedValue.push(<Tag key={tag} value={tag} />);
          }
          index += 1;
        });
      }
    }

    if (shouldCheckExpand) {
      let overMaxLength;
      if (pClass.includes('tag') && value !== '') {
        overMaxLength = this.isTagContentOverMaxLength(finalValue);
      } else {
        overMaxLength = this.isContentOverMaxLength(finalValue);
      }
      if ((overMaxLength && hoverable)) {
        hover = (
          <HoverCell
            onMouseLeave={this.toggleExpand}
            textToRender={expandedValue}
          />
        );
      }
    }

    return (
      <div
        className={divClass}
        onMouseLeave={() => this.toggleExpand(false)}
      >
        <p
          className={pClass}
          data-class={`job-table-cell-with-header-${columnHeader}`}
          onMouseEnter={() => this.toggleExpand(true)}
        >
          {finalValue}
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
  hoverable: PropTypes.bool,
  jobID: PropTypes.string,
  onClickOpenModalJobDetails: PropTypes.func,
  columnHeader: PropTypes.string,
};

InputMetricCell.defaultProps = {
  value: '',
  isError: false,
  cellType: '',
  rowNumber: 0,
  hoverable: true,
  jobID: '',
  onClickOpenModalJobDetails: () => null,
  columnHeader: '',
};

export default InputMetricCell;
