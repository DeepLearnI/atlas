import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';
import Checkbox from '../Checkbox';

class NumberFilter extends Component {
  constructor(props) {
    super(props);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.onChangeMin = this.onChangeMin.bind(this);
    this.onChangeMax = this.onChangeMax.bind(this);
    this.onChangeCheckbox = this.onChangeCheckbox.bind(this);
    this.state = {
      changeHiddenParams: this.props.changeHiddenParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      minValue: this.props.minValue,
      maxValue: this.props.maxValue,
      hideNotAvailable: false,
      columnName: this.props.columnName,
      showAllFilters: false,
    };
  }

  onApply() {
    const {
      changeHiddenParams, toggleShowingFilter, columnName, minValue, maxValue, hideNotAvailable,
    } = this.state;
    changeHiddenParams(minValue, maxValue, hideNotAvailable, columnName);
    toggleShowingFilter();
  }

  onCancel() {
    const { toggleShowingFilter } = this.state;
    toggleShowingFilter();
  }

  onClearFilters() {
    this.setState({ minValue: 0, maxValue: 0, showAllFilters: true });
  }

  onChangeMin(e) {
    this.setState({ minValue: e.target.value });
  }

  onChangeMax(e) {
    this.setState({ maxValue: e.target.value });
  }

  onChangeCheckbox() {
    const { hideNotAvailable } = this.state;
    this.setState({ hideNotAvailable: !hideNotAvailable, showAllFilters: false });
  }

  render() {
    const {
      minValue, maxValue, hideNotAvailable, showAllFilters,
    } = this.state;

    return (
      <div className="filter-container column-filter-container elevation-1 number-filter-container">
        <div className="column-filter-header">
          <button
            type="button"
            onClick={this.onClearFilters}
            className="b--mat b--affirmative text-upper float-right"
          >
          Clear Filters
          </button>
        </div>
        <div className="number-input-container">
          <div>
            <label htmlFor="filter-input-sec">Min</label>
            <input
              type="number"
              id="filter-input-sec"
              placeholder="Min"
              value={minValue}
              onChange={(e) => { this.onChangeMin(e); }}
            />
          </div>
          <div> - </div>
          <div>
            <label htmlFor="filter-input-sec">Max</label>
            <input
              type="number"
              id="filter-input-sec"
              placeholder="Max"
              value={maxValue}
              onChange={(e) => { this.onChangeMax(e); }}
            />
          </div>
        </div>

        <Checkbox
          name="Show 'not available' values"
          hidden={hideNotAvailable}
          changeHiddenParams={this.onChangeCheckbox}
          showAllFilters={showAllFilters}
        />

        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

NumberFilter.propTypes = {
  changeHiddenParams: PropTypes.func,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  minValue: PropTypes.number,
  maxValue: PropTypes.number,
  hideNotAvailable: PropTypes.bool,
  columnName: PropTypes.string,
  showAllFilters: PropTypes.bool,
};

NumberFilter.defaultProps = {
  changeHiddenParams: () => {},
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  minValue: 0,
  maxValue: 0,
  hideNotAvailable: false,
  columnName: '',
  showAllFilters: false,
};

export default NumberFilter;
