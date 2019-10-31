import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";
import MonitorOverview from "./MonitorOverview";
import MonitorJobsTable from "./MonitorJobsTable";
import CommonActions from "../../../actions/CommonActions";

class ScheduleDetails extends Component {
  constructor(props) {
    super(props);

    this.state = {
      monitorResult: {}
    };

    this.reload = this.reload.bind(this);
  }

  componentDidMount() {
    this.reload();
  }

  componentDidUpdate(prevProps) {
    const { selectedMonitor } = this.props;
    if (!CommonActions.deepEqual(selectedMonitor, prevProps.selectedMonitor)) {
      this.reload();
    }
  }

  async reload() {
    const { location, selectedMonitor } = this.props;

    if (location && !CommonActions.isEmptyObject(selectedMonitor)) {
      const projectName = location.state.project.name;
      const monitorResult = await MonitorSchedulesActions.getMonitorList(projectName);
      this.setState({ monitorResult: monitorResult[selectedMonitor.monitorName] });
    } else if (CommonActions.isEmptyObject(selectedMonitor)) {
      this.setState({ monitorResult: {} });
    }
  }

  render() {
    const { monitorResult } = this.state;
    const { location, toggleLogsModal } = this.props;

    let mainRender = (
      <div className="monitor-summary">
        <MonitorOverview monitorResult={monitorResult} />
        <MonitorJobsTable location={location} monitorResult={monitorResult} toggleLogsModal={toggleLogsModal} />
      </div>
    );
    if (!monitorResult || CommonActions.isEmptyObject(monitorResult)) {
      mainRender = (
        <div className="monitor-summary">
          <div className="monitor-details-empty-state">
            <div className="i--icon-clipboard" />
            <div className="monitor-details-empty-state-text">
              Click on a monitor to see its details.
            </div>
          </div>
        </div>
      );
    }

    return mainRender;
  }
}

ScheduleDetails.propTypes = {
  location: PropTypes.object,
  selectedMonitor: PropTypes.object,
  toggleLogsModal: PropTypes.func
};

ScheduleDetails.defaultProps = {
  location: {},
  selectedMonitor: {},
  toggleLogsModal: () => {}
};

export default ScheduleDetails;
