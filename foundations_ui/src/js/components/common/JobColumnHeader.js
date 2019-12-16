import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactTooltip from 'react-tooltip';
import JobListActions from '../../actions/JobListActions';

class JobColumnHeader extends Component {
  constructor(props) {
    super(props);
    this.onClickSort = this.onClickSort.bind(this);
    this.state = {
      title: this.props.title,
      isStatus: this.props.isStatus,
      offsetDivClass: this.props.className,
      containerDivClass: this.props.containerClass,
      mainHeader: this.props.mainHeader,
      isSortedColumn: this.props.isSortedColumn,
      isAscending: this.props.isAscending,
      sortTable: this.props.sortTable,
      selectAllJobs: this.props.selectAllJobs,
      allJobsSelected: this.props.allJobsSelected,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        title: nextProps.title,
        isSortedColumn: nextProps.isSortedColumn,
        isAscending: nextProps.isAscending,
        allJobsSelected: nextProps.allJobsSelected,
      },
    );
  }

  onClickSort() {
    const { sortTable, title, mainHeader } = this.state;

    sortTable(title, mainHeader);
  }

  render() {
    const {
      title, isStatus, offsetDivClass, containerDivClass, isSortedColumn,
      isAscending, selectAllJobs, allJobsSelected, mainHeader,
    } = this.state;
    const headerClassName = JobListActions.getJobColumnHeaderH4Class(isStatus);
    let divClassName = JobListActions.getJobColumnHeaderDivClass(containerDivClass, isStatus);

    let headerName = title;

    if (title === 'Tags') {
      divClassName = 'job-column-header tag-cell';
    }

    if (title === 'SelectAllCheckboxes') {
      headerName = <input type="checkbox" checked={allJobsSelected} onClick={() => { selectAllJobs(); }} />;
    }

    let arrowUp = null;
    let arrowDown = null;
    if (title !== '' && title.toLowerCase() !== 'job id' && title.toLowerCase() !== 'tags'
      && title !== 'SelectAllCheckboxes') {
      arrowUp = (
        <i
          onKeyPress={this.onClickSort}
          tabIndex={0}
          role="button"
          onClick={this.onClickSort}
          className={isSortedColumn && (isAscending === null || isAscending)
            ? 'i--icon-arrow-up' : 'i--icon-arrow-up-unfilled'}
        />
      );
      arrowDown = (
        <i
          onKeyPress={this.onClickSort}
          tabIndex={0}
          role="button"
          onClick={this.onClickSort}
          className={isSortedColumn && (isAscending === null || !isAscending)
            ? 'i--icon-arrow-down' : 'i--icon-arrow-down-unfilled'}
        />
      );
    }

    let dataClass = '';

    if (mainHeader === 'Metrics') {
      dataClass = 'metric-header';
    } else if (mainHeader === 'Parameters') {
      dataClass = 'param-header';
    }

    return (
      <div
        className={divClassName}
        ref={c => { this.headerContainer = c; }}
        data-class={dataClass}
      >
        <div className={offsetDivClass}>
          <h4
            className={`${headerClassName}`}
            data-tip={typeof (headerName) === 'string' && headerName.length > 15 ? headerName : ''}
          >
            {headerName}
            <ReactTooltip place="top" type="dark" effect="solid" />
          </h4>
          {arrowUp}
          {arrowDown}
        </div>
      </div>
    );
  }
}

JobColumnHeader.propTypes = {
  title: PropTypes.string,
  isStatus: PropTypes.bool,
  className: PropTypes.string,
  containerClass: PropTypes.string,
  toggleFilter: PropTypes.func,
  colType: PropTypes.string,
  isMetric: PropTypes.bool,
  isSortedColumn: PropTypes.bool,
  isAscending: PropTypes.bool,
  sortTable: PropTypes.func,
  selectAllJobs: PropTypes.func,
  allJobsSelected: PropTypes.bool,
  mainHeader: PropTypes.string,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: false,
  className: '',
  containerClass: 'job-column-header',
  toggleFilter: () => {},
  colType: 'string',
  isMetric: false,
  isSortedColumn: false,
  isAscending: false,
  sortTable: () => {},
  selectAllJobs: () => {},
  allJobsSelected: false,
  mainHeader: '',
};

export default JobColumnHeader;
