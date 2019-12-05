import React, { Component } from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import HoverCell from './HoverCell';
import JobListActions from '../../../actions/JobListActions';
import CommonActions from '../../../actions/CommonActions';


class StartTimeCell extends Component {
  constructor(props) {
    super(props);
    this.toggleExpand = this.toggleExpand.bind(this);
    this.state = {
      date: JobListActions.getFormatedDate(this.props.startTime),
      time: JobListActions.getFormatedTime(this.props.startTime),
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
      expand: this.props.expand,
      status: this.props.status,
    };
  }

  toggleExpand(value) {
    this.setState({ expand: value });
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.rowNumber !== this.props.rowNumber) {
      this.setState({
        time: JobListActions.getFormatedTime(nextProps.startTime),
        date: JobListActions.getFormatedDate(nextProps.startTime),
        rowNumber: nextProps.rowNumber,
        isError: nextProps.isError,
        expand: nextProps.expand,
        status: nextProps.status,
      });
    }
  }


  render() {
    const {
      date, time, isError, rowNumber, expand, status,
    } = this.state;
    let hover;

    const errorClass = CommonActions.errorStatus(isError);
    const spanClass = ''.concat(errorClass);

    const pClass = isError
      ? `job-cell start-cell error row-${rowNumber}`
      : `job-cell start-cell row-${rowNumber}`;

    const launchDate = status === 'queued' ? 'Queued' : moment(date).format('MMM DD').toString();
    const launchTime = status === 'queued' ? '' : time;

    const dateTimeFormatted = (
      <span className="font-bold">
        <span className="launch-date">{launchDate} </span>
        <span className={spanClass}>{launchTime}</span>
      </span>
    );

    if (expand && date !== '') {
      hover = <HoverCell textToRender={dateTimeFormatted} />;
    }

    return (
      <span
        key={`${date}-${time}`}
        onMouseEnter={() => this.toggleExpand(true)}
        onMouseLeave={() => this.toggleExpand(false)}
      >
        {dateTimeFormatted}
        <span>{hover}</span>
      </span>
    );
  }
}

StartTimeCell.propTypes = {
  startTime: PropTypes.string,
  isError: PropTypes.bool,
  rowNumber: PropTypes.number,
  expand: PropTypes.bool,
  status: PropTypes.string,
};

StartTimeCell.defaultProps = {
  startTime: '',
  isError: false,
  rowNumber: -1,
  expand: false,
  status: '',
};

export default StartTimeCell;
