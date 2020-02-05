import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Flatpickr from 'react-flatpickr';
import CommonActions from '../../../actions/CommonActions';

class DateTimeFilter extends Component {
  constructor(props) {
    super(props);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.onChangeDateTime = this.onChangeDateTime.bind(this);
    this.isDisabled = this.isDisabled.bind(this);
    this.state = {
      changeHiddenParams: this.props.changeHiddenParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      startDate: this.props.startDate,
      endDate: this.props.endDate,
      isStartPickerOpen: false,
      isEndPickerOpen: false,
    };
  }

  onApply() {
    const {
      changeHiddenParams, toggleShowingFilter, startDate, endDate,
    } = this.state;
    if (!this.isDisabled()) {
      changeHiddenParams(startDate, endDate);
      toggleShowingFilter();
    }
  }

  async onCancel() {
    const { toggleShowingFilter } = this.state;
    await this.onClearFilters();
    toggleShowingFilter();
  }

  async onClearFilters() {
    await this.setState({
      startDate: null,
      endDate: null,
    });
  }

  async onChangeDateTime(e, isStartTime) {
    if (isStartTime) {
      await this.setState({ startDate: new Date(e[0]) });
    } else {
      await this.setState({ endDate: new Date(e[0]) });
    }
  }

  isDisabled() {
    const { startDate, endDate } = this.state;
    return startDate > endDate || startDate === null || endDate === null;
  }

  render() {
    const {
      startDate, endDate, isStartPickerOpen, isEndPickerOpen,
    } = this.state;

    let startCalButton = (
      <div
        className="i--icon-cal-clock"
        role="presentation"
      />
    );
    if (isStartPickerOpen) {
      startCalButton = (
        <div
          className="i--icon-cal-clock"
          role="presentation"
        />
      );
    }

    let endCalButton = (
      <div
        className="i--icon-cal-clock"
        role="presentation"
      />
    );
    if (isEndPickerOpen) {
      endCalButton = (
        <div
          className="i--icon-cal-clock"
          role="presentation"
        />
      );
    }

    const applyClass = CommonActions.getApplyClass(this.isDisabled);

    return (
      <div className="filter-container column-filter-container elevation-1 datetime-filter-container">
        <div className="column-filter-header">
          <p>between</p>
          <button
            type="button"
            onClick={this.onClearFilters}
            className="b--mat b--affirmative text-upper float-right"
          >
            Clear Filters
          </button>
        </div>
        <div className="date-time-picker">
          {startCalButton}
          <Flatpickr
            data-enable-time
            ref={startPicker => { this.startPicker = startPicker; }}
            value={startDate}
            onChange={e => { this.onChangeDateTime(e, true); }}
          />
        </div>
        <p>and</p>
        <div className="date-time-picker">
          {endCalButton}
          <Flatpickr
            data-enable-time
            value={endDate}
            ref={endPicker => { this.endPicker = endPicker; }}
            onChange={e => { this.onChangeDateTime(e, false); }}
          />
        </div>
        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className={applyClass}>Apply</button>
        </div>
      </div>
    );
  }
}

DateTimeFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  startDate: PropTypes.object,
  endDate: PropTypes.object,
  isStartPickerOpen: PropTypes.bool,
  isEndPickerOpen: PropTypes.bool,
};

DateTimeFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  startDate: null,
  endDate: null,
  isStartPickerOpen: false,
  isEndPickerOpen: false,
};

export default DateTimeFilter;
