import React from 'react';
import moment from 'moment';
import Cookies from 'js-cookie';
import JobColumnHeader from '../components/common/JobColumnHeader';
import InputMetricCell from '../components/common/InputMetricCell';
import InputMetricRow from '../components/common/InputMetricRow';
import Checkbox from '../components/common/Checkbox';
import JobListActions from './JobListActions';

const notFound = -1;
const oneElement = 1;

class CommonActions {
  // Helper Functions
  static getInputMetricColumnHeaders(
    allInputParams, hiddenInputParams, toggleNumberFilter, isMetric, filteredArray, sortedColumn, sortTable,
    selectAllJobs, allJobsSelected, header,
  ) {
    if (allInputParams.length > 0) {
      return this.getInputParamHeaders(
        allInputParams, hiddenInputParams, toggleNumberFilter, isMetric, filteredArray, sortedColumn,
        sortTable, selectAllJobs, allJobsSelected, header,
      );
    }
    return null;
  }

  static getInputParamHeaders(
    allInputParams, hiddenInputParams, toggleNumberFilter, isMetric, filteredArray, sortedColumn, sortTable,
    selectAllJobs, allJobsSelected, header,
  ) {
    const inputParams = [];
    allInputParams.forEach(input => {
      if (this.arrayDoesNotInclude(hiddenInputParams, input.name)) {
        const key = input.name;
        const colType = input.type;
        const isFiltered = JobListActions.isColumnFiltered(filteredArray, key);

        let { column } = sortedColumn;
        if (column.startsWith('job_parameters')) {
          column = column.substring('job_parameters:'.length);
        }
        if (column.startsWith('output_metrics')) {
          column = column.substring('output_metrics:'.length);
        }

        const isSorted = column === key || column === '';
        const isAscending = column === '' ? null : sortedColumn.isAscending;
        inputParams.push(<JobColumnHeader
          key={key}
          title={key}
          className="inline-block full-width"
          containerClass="job-column-header"
          toggleFilter={toggleNumberFilter}
          colType={colType}
          isMetric={isMetric}
          isFiltered={isFiltered}
          isSortedColumn={isSorted}
          isAscending={isAscending}
          sortTable={sortTable}
          selectAllJobs={selectAllJobs}
          allJobsSelected={allJobsSelected}
          mainHeader={header}
        />);
      }
    });
    return inputParams;
  }

  static formatAMPM(date) {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    const amOrPm = hours >= 12 ? 'PM' : 'AM';
    hours %= 12;
    hours = hours || 12;
    minutes = minutes < 10 ? `0${minutes}` : minutes;
    const strTime = `${hours}:${minutes} ${amOrPm}`;
    return strTime;
  }

  static getInputMetricCells(job, isError, isMetric, columns, hiddenInputParams,
    rowNumber, onClickOpenModalJobDetails, isSelected) {
    if (isMetric && job.output_metrics) {
      return this.getMetricCellsFromOutputMetrics(job, isError, columns, isMetric, hiddenInputParams,
        rowNumber, onClickOpenModalJobDetails, isSelected);
    }

    if (!isMetric && job.job_parameters) {
      return this.getInputCellsFromInputParams(job, isError, columns, isMetric, hiddenInputParams,
        rowNumber, onClickOpenModalJobDetails);
    }
    return null;
  }

  static getInputCellsFromInputParams(job, isError, columns, isMetric, hiddenInputParams,
    rowNumber, onClickOpenModalJobDetails) {
    let cells = [];
    cells = [];
    columns.forEach(col => {
      if (this.arrayDoesNotInclude(hiddenInputParams, col)) {
        const input = this.getInputMetricInput(job.job_parameters, col, isMetric);
        const key = this.getInputMetricKey(input, col, isMetric);
        let inputValue = JobListActions.getInputMetricValue(input, isMetric, columns);
        const cellType = this.getInputMetricCellType(input);
        const isHoverable = this.getInputMetricIsHoverable(input);

        if (cellType.match(/array*/)) {
          inputValue = this.transformArraysToString(inputValue);
        }

        const openModalJobDetails = jobID => {
          onClickOpenModalJobDetails(job);
        };

        cells.push(<InputMetricCell
          key={key}
          columnHeader={key}
          value={inputValue}
          isError={isError}
          cellType={cellType}
          rowNumber={rowNumber}
          hoverable={isHoverable}
          jobID={job.job_id}
          onClickOpenModalJobDetails={openModalJobDetails}
        />);
      }
    });
    return cells;
  }

  static getMetricCellsFromOutputMetrics(job, isError, columns, isMetric, hiddenInputParams,
    rowNumber, onClickOpenModalJobDetails) {
    const cells = [];
    columns.forEach(col => {
      if (this.arrayDoesNotInclude(hiddenInputParams, col)) {
        const input = this.getInputMetricInput(job.output_metrics, col, isMetric);
        let inputValue = JobListActions.getInputMetricValue(input, isMetric, columns);
        const key = this.getInputMetricKey(input, col, isMetric);
        const cellType = this.getInputMetricCellType(input);
        const isHoverable = this.getInputMetricIsHoverable(input);
        if (cellType.match(/array*/)) {
          inputValue = this.transformArraysToString(inputValue);
        }

        const openModalJobDetails = jobID => {
          onClickOpenModalJobDetails(job);
        };

        cells.push(<InputMetricCell
          key={key}
          columnHeader={key}
          value={inputValue}
          isError={isError}
          cellType={cellType}
          rowNumber={rowNumber}
          hoverable={isHoverable}
          jobID={job.job_id}
          onClickOpenModalJobDetails={openModalJobDetails}
        />);
      } else {
        cells.push(null);
      }
    });
    return cells;
  }

  static transformArraysToString(arrayValue) {
    let newValue = '[';
    arrayValue.forEach(element => {
      newValue = newValue.concat(String(element));
      newValue += ', ';
    });
    newValue = newValue.slice(0, newValue.length - 2);
    newValue += ']';
    return newValue;
  }

  static getInputMetricRows(jobs, isMetric, allInputMetricColumn, hiddenInputParams,
    onMetricRowClick, onClickOpenModalJobDetails) {
    let rows = null;
    let rowNumber = 0;
    if (jobs.length > 0) {
      rows = [];
      jobs.forEach(job => {
        const key = this.getRowKey(job);
        const isError = this.isError(job.status);
        rows.push(<InputMetricRow
          key={key}
          job={job}
          isError={isError}
          isMetric={isMetric}
          allInputMetricColumn={allInputMetricColumn}
          hiddenInputParams={hiddenInputParams}
          rowNumber={rowNumber}
          onMetricRowClick={onMetricRowClick}
          onClickOpenModalJobDetails={onClickOpenModalJobDetails}
        />);
        rowNumber += 1;
      });
    }
    return rows;
  }

  static getInputMetricCellPClass(isError, cellType) {
    return isError ? `error type-${cellType}` : `type-${cellType}`;
  }

  static getInputMetricCellDivClass(isError, rowNumber, key) {
    return isError ? `job-cell error row-${rowNumber} key-${key}` : `job-cell row-${rowNumber} key-${key}`;
  }

  static isError(status) {
    return status.toLowerCase() === 'failed';
  }

  static errorStatus(isError) {
    return isError ? 'failed' : '';
  }

  static formatColumns(columns, hiddenInputParams, searchText = '') {
    const formattedColumns = [];
    if (columns !== null) {
      columns.forEach(col => {
        if (col.name.toLowerCase().includes(searchText.toLowerCase())) {
          let isHidden = false;
          if (hiddenInputParams.includes(col.name)) {
            isHidden = true;
          }
          formattedColumns.push({ name: col.name, hidden: isHidden });
        }
      });
    }
    return formattedColumns;
  }

  static getChangedCheckboxes(changedParams, colName) {
    const index = changedParams.indexOf(colName);
    const copyArray = this.deepCopyArray(changedParams);
    if (index !== notFound) {
      copyArray.splice(index, oneElement);
    } else {
      copyArray.push(colName);
    }
    return copyArray;
  }

  static getRowKey(job) {
    return job.job_id.concat('-input-metric-row');
  }


  static getInputMetricCellType(inputMetric) {
    if (inputMetric && inputMetric.type) {
      return inputMetric.type;
    }
    return 'not-available';
  }

  static getInputMetricIsHoverable(inputMetric) {
    if (inputMetric && inputMetric.hoverable !== undefined) {
      return inputMetric.hoverable;
    }
    return true;
  }

  static getFlatArray(array) {
    return array.map(element => {
      return element.name;
    });
  }

  static getOldFiltersWithoutColumn(oldFilters, newColumnName) {
    return oldFilters.filter(
      filter => {
        if (filter.columnName !== newColumnName) {
          return true;
        }
      },
    );
  }

  static getNumberFilters(oldFilters, newMin, newMax, newShowingNotAvailable, newColumnName) {
    const newFilters = this.getOldFiltersWithoutColumn(oldFilters, newColumnName);
    newFilters.push({
      columnName: newColumnName,
      min: newMin,
      max: newMax,
      showingNotAvailable: newShowingNotAvailable,
    });
    return newFilters;
  }

  static getContainFilters(oldFilters, newSearchText, newColumnName) {
    const newFilters = this.getOldFiltersWithoutColumn(oldFilters, newColumnName);
    newFilters.push({
      columnName: newColumnName,
      searchText: newSearchText,
    });
    return newFilters;
  }

  static getBoolFilters(oldFilters, newFormattedBool, newColumnName) {
    const newFilters = this.getOldFiltersWithoutColumn(oldFilters, newColumnName);
    newFilters.push({
      columnName: newColumnName,
      boolCheckboxes: newFormattedBool,
    });
    return newFilters;
  }

  static getDurationFilters(startTime, endTime, columnName) {
    return [{ columnName: columnName, startTime: startTime, endTime: endTime }];
  }

  static getApplyClass(isDisabled) {
    let applyClass = 'b--mat b--affirmative text-upper';
    if (isDisabled()) {
      applyClass += ' b--disabled';
    }
    return applyClass;
  }

  static getInputMetricFilterLeft(metricClass) {
    let style = null;
    const inputBorder = 3;
    if (this.isMetricAndHasContainers(metricClass)) {
      const staticColumnLeft = document.getElementsByClassName('job-static-columns-container')[0].clientWidth;
      const inputParamLeft = document.getElementsByClassName('job-static-columns-container')[1].clientWidth;

      const filterLeft = staticColumnLeft + inputParamLeft + inputBorder;
      style = { left: filterLeft };
    }
    return style;
  }

  static isMetricAndHasContainers(metricClass) {
    return (metricClass === 'is-metric' && document.getElementsByClassName('job-static-columns-container').length > 1);
  }

  // private functions, not cannot declare a private and static
  // function in JS https://stackoverflow.com/a/3218950
  static arrayDoesNotInclude(array, value) {
    return !array.includes(value);
  }

  static getInputMetricInput(jobArray, column, isMetric) {
    let input = null;
    if (!isMetric) {
      input = {};
    }
    if (jobArray) {
      jobArray.forEach(param => {
        if (param.name === column) {
          input = param;
        }
      });
    }
    return input;
  }

  static getInputMetricKey(input, colIndex, isMetric) {
    if (isMetric) {
      let key = 'metric-'.concat(colIndex);
      if (input && input.name) {
        key = input.name;
      }
      return key;
    }
    let key = 'input-param-'.concat(colIndex);
    if (input && input.name) {
      key = input.name;
    }
    return key;
  }

  static getCheckboxes(
    columns, changeLocalParams, showAllFilters, unsetClearFilters, hideAllFilters,
    statusCheckbox = false, unsetHideFilters = () => {},
  ) {
    let checkboxes = [];
    let hasSeenParams = false;
    if (columns.length > 0) {
      checkboxes = [];
      checkboxes.push(<h3 className="column-filter-divider">Metrics</h3>);
      columns.forEach(col => {
        if (col.header === 'parameter' && !hasSeenParams) {
          checkboxes.push(<h3 className="column-filter-divider">Parameters</h3>);
          hasSeenParams = true;
        }
        let statusCircle = null;
        if (statusCheckbox) {
          statusCircle = JobListActions.getStatusCircle(col.name);
        }
        const key = col.name.concat('-checkbox');
        checkboxes.push(<Checkbox
          key={key}
          name={col.name}
          hidden={col.hidden}
          changeHiddenParams={changeLocalParams}
          showAllFilters={showAllFilters}
          unsetClearFilters={unsetClearFilters}
          statusCircle={statusCircle}
          hideAllFilters={hideAllFilters}
          unsetHideFilters={unsetHideFilters}
        />);
      });
    }
    return checkboxes;
  }

  static deepCopyArray(originalArray) {
    return JSON.parse(JSON.stringify(originalArray));
  }

  static formatDate(date) {
    date = new Date(date);
    return `${moment(JobListActions.getFormatedDate(date)).format('MMM DD').toString()}
            ${JobListActions.getFormatedTime(date)}`;
  }

  static getTagsFromJob(jobs) {
    const set = new Set();
    jobs.forEach(job => {
      if (job.tags) {
        if (Array.isArray(job.tags)) {
          job.tags.forEach(tag => {
            set.add(tag);
          });
        } else {
          const keys = Object.keys(job.tags);
          keys.forEach(tag => {
            set.add(tag);
          });
        }
      }
    });
    const tags = Array.from(set);
    return tags;
  }

  static getAccessCookie() {
    return Cookies.get('atlas_access_token');
  }

  static checkStatusResponse(response) {
    if (response.status === 401) {
      window.location = '/login';
    }
  }
}

export default CommonActions;
