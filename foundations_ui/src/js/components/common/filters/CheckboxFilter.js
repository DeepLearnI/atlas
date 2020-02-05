import React, { Component } from 'react';
import PropTypes from 'prop-types';

class CheckboxFilter extends Component {
  constructor(props) {
    super(props);
    this.state = {
      checkboxes: this.props.checkboxes,
      onCancel: this.props.onCancel,
      onApply: this.props.onApply,
      submitSearchText: this.props.submitSearchText,
      onClearFilters: this.props.onClearFilters,
      input: this.props.input,
      addedClass: this.props.addedClass,
      applyClass: this.props.applyClass,
      onHideAll: this.props.onHideAll,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ checkboxes: nextProps.checkboxes, applyClass: nextProps.applyClass });
  }

  render() {
    const {
      checkboxes, onCancel, onApply, submitSearchText, onClearFilters, input, addedClass, applyClass, onHideAll,
    } = this.state;

    const divClass = 'filter-container column-filter-container elevation-1 '.concat(addedClass);

    return (
      <div className={divClass}>
        <div className="column-filter-header">
          {input}
          <button
            className="button-icon"
            type="button"
            onClick={submitSearchText}
            onKeyPress={submitSearchText}
          >
            <div className="magnifying-glass" />
          </button>
          <div className="column-control-buttons">
            <button
              type="button"
              onClick={onHideAll}
              className="b--mat b--negation text-upper"
            >
              SELECT NONE
            </button>
            <button
              type="button"
              onClick={onClearFilters}
              className="b--mat b--negation-grey grey text-upper"
            >
              SELECT ALL
            </button>
          </div>
        </div>
        {checkboxes.length === 0
        && (
          <div className="column-filter-list empty">
            <div className="column-filter-image-empty">
              <div className="container-text-empty">
                <div className="column-filter-text-empty">
                  <p className="font-bold">No parameters or metric columns</p>
                  <p className="font-bold">available to filter.</p>
                </div>
                <div className="column-filter-text-empty">
                  <p>Log some metrics or parameters</p>
                  <p>on your next job run.</p>
                </div>
              </div>
            </div>
          </div>
        )}
        {checkboxes.length > 0
        && (
          <div className="column-filter-list">
            {checkboxes}
          </div>
        )}
        <div className="column-filter-buttons">
          <button type="button" onClick={onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={onApply} className="b--mat b--negation-grey grey text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

CheckboxFilter.propTypes = {
  checkboxes: PropTypes.array,
  onCancel: PropTypes.func,
  onApply: PropTypes.func,
  submitSearchText: PropTypes.func,
  onClearFilters: PropTypes.func,
  input: PropTypes.object,
  addedClass: PropTypes.string,
  applyClass: PropTypes.string,
  onHideAll: PropTypes.func,
};

CheckboxFilter.defaultProps = {
  checkboxes: [],
  onCancel: () => {},
  onApply: () => {},
  submitSearchText: () => {},
  onClearFilters: () => {},
  input: null,
  addedClass: '',
  applyClass: 'b--mat b--affirmative text-upper',
  onHideAll: () => {},
};

export default CheckboxFilter;
