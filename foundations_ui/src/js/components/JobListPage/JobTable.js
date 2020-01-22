import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTableHeader from './JobTableHeader';
import JobTableButtons from './JobTableButtons';
import rowSelect from '../../../scss/jquery/rowSelect';


class JobTable extends Component {
  constructor(props) {
    super(props);
    this.onDataUpdated = props.onDataUpdated.bind(this);
    this.onClickOpenModalJobDetails = this.onClickOpenModalJobDetails.bind(this);
    this.updateFilterSearchText = this.updateFilterSearchText.bind(this);
    this.filterColumns = this.filterColumns.bind(this);
    this.updateHiddenColumns = this.updateHiddenColumns.bind(this);
    this.sortTable = this.sortTable.bind(this);
    this.selectJob = this.selectJob.bind(this);
    this.selectAllJobs = this.selectAllJobs.bind(this);
    this.selectNoJobs = this.selectNoJobs.bind(this);
    this.state = {
      jobs: this.props.jobs,
      isLoaded: this.props.isLoaded,
      allInputParams: this.props.allInputParams,
      allMetrics: this.props.allMetrics,
      statuses: this.props.statuses,
      updateHiddenStatus: this.props.updateHiddenStatus,
      updateHiddenUser: this.props.updateHiddenUser,
      updateNumberFilter: this.props.updateNumberFilter,
      updateContainsFilter: this.props.updateContainsFilter,
      updateBoolFilter: this.props.updateBoolFilter,
      updateDurationFilter: this.props.updateDurationFilter,
      updateJobIdFilter: this.props.updateJobIdFilter,
      updateStartTimeFilter: this.props.updateStartTimeFilter,
      allUsers: this.props.allUsers,
      hiddenUsers: this.props.hiddenUsers,
      numberFilters: this.props.numberFilters,
      boolFilters: this.props.boolFilters,
      boolCheckboxes: this.props.boolCheckboxes,
      durationFilters: this.props.durationFilters,
      jobIdFilters: this.props.jobIdFilters,
      startTimeFilters: this.props.startTimeFilters,
      filters: this.props.filters,
      filterSearchText: '',
      filteredColumns: null,
      hiddenColumns: [],
      sortedColumn: { column: '', isAscending: true },
      selectedJobs: [],
      allJobsSelected: false,
      projectName: this.props.projectName,
      getJobs: this.props.getJobs,
      reload: this.props.reload,
      tensorboardEnabled: false,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        statuses: nextProps.statuses,
        jobs: nextProps.jobs,
        isLoaded: nextProps.isLoaded,
        allInputParams: nextProps.allInputParams,
        allMetrics: nextProps.allMetrics,
        allUsers: nextProps.allUsers,
        hiddenUsers: nextProps.hiddenUsers,
        boolCheckboxes: nextProps.boolCheckboxes,
        numberFilters: nextProps.numberFilters,
        boolFilters: nextProps.boolFilters,
        durationFilters: nextProps.durationFilters,
        jobIdFilters: nextProps.jobIdFilters,
        startTimeFilters: nextProps.startTimeFilters,
        filters: nextProps.filters,
        projectName: nextProps.projectName,
      },
    );
  }

  handleRowSelection(rowNumber) {
    const { selectedRow } = this.state;
    if (selectedRow === rowNumber) {
      this.setState({ selectedRow: -1 });
      rowSelect.deselect(rowNumber);
    } else {
      rowSelect.select(rowNumber);
      this.setState({ selectedRow: rowNumber });
    }
  }

  closeSideBar() {
    this.setState({ selectedRow: -1 });
    rowSelect.removePreviousActiveRows();
  }

  onClickOpenModalJobDetails(job) {
    const { onClickJob } = this.props;
    onClickJob(job);
    this.handleRowSelection(job.job_id);
  }

  async updateFilterSearchText(newText) {
    await this.setState({ filterSearchText: newText });
    this.filterColumns();
  }

  filterColumns() {
    const { filterSearchText, allMetrics, allInputParams } = this.state;
    const allFilterableColumns = allMetrics.concat(allInputParams);
    if (filterSearchText.trim().length > 0) {
      const filteredColumns = allFilterableColumns.filter(col => {
        return col.name.includes(filterSearchText);
      });
      this.setState({ filteredColumns: filteredColumns });
    } else {
      this.setState({ filteredColumns: allFilterableColumns });
    }
  }

  updateHiddenColumns(newHidden) {
    this.setState({ hiddenColumns: newHidden });
  }

  sortTable(clickedColumn, mainHeader) {
    const { sortedColumn, getJobs } = this.state;

    let clickedColumnWithMainHeader = clickedColumn;
    let isAscending = true;

    if (mainHeader === 'Parameters') {
      clickedColumnWithMainHeader = `parameters:${clickedColumn}`;
    }
    if (mainHeader === 'Metrics') {
      clickedColumnWithMainHeader = `output_metrics:${clickedColumn}`;
    }

    if (clickedColumnWithMainHeader === sortedColumn.column) {
      if (sortedColumn.isAscending === true) {
        clickedColumnWithMainHeader = '';
      }
    } else {
      isAscending = false;
    }

    this.setState({ sortedColumn: { column: clickedColumnWithMainHeader, isAscending: isAscending } }, () => {
      getJobs(this.state.sortedColumn);
    });
  }

  selectJob(jobID) {
    const { selectedJobs, jobs } = this.state;
    let newSelectedJobs = Array.from(selectedJobs);
    if (selectedJobs.includes(jobID)) {
      newSelectedJobs = newSelectedJobs.filter(job => {
        return job !== jobID;
      });
    } else {
      newSelectedJobs.push(jobID);
      const selectedJob = jobs.find(job => {
        return job.job_id === jobID;
      });
    }
    let newAllJobsSelected = false;
    if (jobs.length === newSelectedJobs.length) {
      newAllJobsSelected = true;
    }

    const newTensorboardEnabled = this.canGoToTensorboard(newSelectedJobs);

    this.setState({
      selectedJobs: newSelectedJobs,
      allJobsSelected: newAllJobsSelected,
      tensorboardEnabled: newTensorboardEnabled,
    });
  }

  canGoToTensorboard(newSelectedJobs) {
    const { jobs } = this.state;
    const jobsByID = {};
    jobs.forEach(job => {
      jobsByID[job.job_id] = job;
    });
    const selectedJobObjects = newSelectedJobs.map(singleJobID => {
      return jobsByID[singleJobID];
    });
    return !!selectedJobObjects.length && selectedJobObjects.every(job => {
      return !!job.tags.tf;
    });
  }

  selectAllJobs() {
    const { jobs, selectedJobs, allJobsSelected } = this.state;
    let jobIds = [];
    let areAllSelected = false;
    if (selectedJobs.length !== jobs.length) {
      jobIds = jobs.map(job => {
        return job.job_id;
      });
      areAllSelected = true;
    }
    const newTensorboardEnabled = this.canGoToTensorboard(jobIds);
    this.setState({
      selectedJobs: jobIds,
      allJobsSelected: areAllSelected,
      tensorboardEnabled: newTensorboardEnabled,
    });
  }

  selectNoJobs() {
    this.setState({ selectedJobs: [], allJobsSelected: false });
  }

  render() {
    const {
      jobs, isLoaded, allInputParams, allMetrics, statuses, updateHiddenStatus, updateHiddenUser, allUsers, hiddenUsers,
      updateNumberFilter, numberFilters, updateContainsFilter, cotainFilters, updateBoolFilter, boolFilters,
      boolCheckboxes, updateDurationFilter, durationFilters, updateJobIdFilter, jobIdFilters, updateStartTimeFilter,
      startTimeFilters, filters, filteredColumns, hiddenColumns, sortedColumn, selectedJobs, allJobsSelected,
      projectName, getJobs, reload, tensorboardEnabled,
    } = this.state;

    const jobRows = [];
    const rowNum = 1;
    const rowNumbers = [];

    const handleClick = job => {};

    const allFilterableColumns = allMetrics.concat(allInputParams);
    const visibleMetrics = allMetrics.filter(col => {
      return !hiddenColumns.includes(col.name);
    });
    const visibleParams = allInputParams.filter(col => {
      return !hiddenColumns.includes(col.name);
    });

    const curVisibleColumns = filteredColumns !== null && filteredColumns.length < allFilterableColumns.length
      ? filteredColumns : allFilterableColumns;

    curVisibleColumns.forEach(col => {
      if (hiddenColumns.includes(col.name)) {
        col.hidden = true;
      } else {
        col.hidden = false;
      }
    });

    return (
      <div className="job-table-content">
        <div className="job-table-container">
          <JobTableButtons
            columns={curVisibleColumns}
            updateSearchText={this.updateFilterSearchText}
            hiddenColumns={hiddenColumns}
            updateHiddenColumns={this.updateHiddenColumns}
            selectAllJobs={this.selectAllJobs}
            selectedJobs={selectedJobs}
            projectName={projectName}
            getJobs={getJobs}
            selectNoJobs={this.selectNoJobs}
            reload={reload}
            buttonTensorboardEnabled={tensorboardEnabled}
          />
          <JobTableHeader
            allInputParams={visibleParams}
            allMetrics={visibleMetrics}
            jobs={jobs}
            statuses={statuses}
            updateHiddenStatus={updateHiddenStatus}
            rowNumbers={rowNumbers}
            jobRows={jobRows}
            updateHiddenUser={updateHiddenUser}
            allUsers={allUsers}
            hiddenUsers={hiddenUsers}
            boolCheckboxes={boolCheckboxes}
            updateNumberFilter={updateNumberFilter}
            numberFilters={numberFilters}
            updateContainsFilter={updateContainsFilter}
            updateBoolFilter={updateBoolFilter}
            boolFilters={boolFilters}
            updateDurationFilter={updateDurationFilter}
            durationFilters={durationFilters}
            updateJobIdFilter={updateJobIdFilter}
            jobIdFilters={jobIdFilters}
            updateStartTimeFilter={updateStartTimeFilter}
            startTimeFilters={startTimeFilters}
            filters={filters}
            onMetricRowClick={handleClick}
            onDataUpdated={this.onDataUpdated}
            onClickOpenModalJobDetails={this.onClickOpenModalJobDetails}
            sortedColumn={sortedColumn}
            sortTable={this.sortTable}
            selectJob={this.selectJob}
            selectAllJobs={this.selectAllJobs}
            selectedJobs={selectedJobs}
            allJobsSelected={allJobsSelected}
          />
          {/* <div className="pagination-controls">
            <p><span className="font-bold">Viewing:</span> 1-100/600</p>
            <div className="arrow-right" />
            <p>Page 1</p>
            <div className="arrow-left" />
          </div> */}
        </div>
      </div>
    );
  }
}

JobTable.propTypes = {
  isMount: PropTypes.bool,
  jobs: PropTypes.array,
  isLoaded: PropTypes.bool,
  projectName: PropTypes.string,
  allInputParams: PropTypes.array,
  allMetrics: PropTypes.array,
  updateHiddenStatus: PropTypes.func,
  statuses: PropTypes.array,
  updateHiddenUser: PropTypes.func,
  allUsers: PropTypes.array,
  hiddenUsers: PropTypes.array,
  updateNumberFilter: PropTypes.func,
  numberFilters: PropTypes.array,
  updateContainsFilter: PropTypes.func,
  containFilters: PropTypes.array,
  updateBoolFilter: PropTypes.func,
  boolFilters: PropTypes.array,
  boolCheckboxes: PropTypes.array,
  updateDurationFilter: PropTypes.func,
  durationFilters: PropTypes.array,
  updateJobIdFilter: PropTypes.func,
  jobIdFilters: PropTypes.array,
  updateStartTimeFilter: PropTypes.func,
  startTimeFilters: PropTypes.array,
  filters: PropTypes.array,
  selectedRow: PropTypes.string,
  onDataUpdated: PropTypes.func,
  onClickJob: PropTypes.func,
  getJobs: PropTypes.func,
  reload: PropTypes.func,
};

JobTable.defaultProps = {
  isMount: false,
  jobs: [],
  isLoaded: false,
  projectName: '',
  allInputParams: [],
  allMetrics: [],
  updateHiddenStatus: () => {},
  statuses: [],
  updateHiddenUser: () => {},
  allUsers: [],
  hiddenUsers: [],
  updateNumberFilter: () => {},
  numberFilters: [],
  updateContainsFilter: () => {},
  containFilters: [],
  updateBoolFilter: () => {},
  boolFilters: [],
  boolCheckboxes: [],
  updateDurationFilter: () => {},
  durationFilters: [],
  updateJobIdFilter: () => {},
  jobIdFilters: [],
  updateStartTimeFilter: () => {},
  startTimeFilters: [],
  filters: [],
  selectedRow: -1,
  onDataUpdated: () => window.location.reload(),
  onClickJob: job => {},
  getJobs: () => {},
  reload: () => {},
};

export default JobTable;
