import React from 'react';
import PropTypes from 'prop-types';
import Notes from './Notes';
import Readme from './Readme';
import JobOverviewGraph from './JobOverviewGraph';
import BaseActions from '../../actions/BaseActions';

class ProjectOverview extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      projectName: this.props.match.params.projectName,
      metric: '',
      allMetrics: [],
      graphData: [],
      timerId: -1,
    };
    this.setMetric = this.setMetric.bind(this);
  }

  async reload() {
    const { projectName, metric } = this.state;
    let URL = `projects/${projectName}/overview_metrics`;
    if (metric) {
      URL = `${URL}?metric_name=${metric}`;
    }

    const APIGraphData = await BaseActions.getFromStaging(URL);

    if (APIGraphData.length > 0) {
      const allMetrics = APIGraphData.map((graphMetric) => {
        return graphMetric.metric_name;
      });
      this.setState({ graphData: APIGraphData[0].values, metric: APIGraphData[0].metric_name, allMetrics });
    }
  }

  componentDidMount() {
    this.reload();
    const value = setInterval(() => {
      this.reload();
    }, 20000);
    this.setState({
      timerId: value,
    });
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  async setMetric(newMetric) {
    await this.setState({ metric: newMetric });
    this.reload();
  }

  render() {
    const {
      metric, graphData, allMetrics,
    } = this.state;

    return (
      <div className="dashboard-content-container row">
        <section className="chart-and-notes col-md-8">
          <JobOverviewGraph metric={metric} graphData={graphData} allMetrics={allMetrics} setMetric={this.setMetric} />
          <Readme {...this.props} />
        </section>
        <Notes {...this.props} />
      </div>
    );
  }
}

ProjectOverview.propTypes = {
  history: PropTypes.object,
  match: PropTypes.object,
};

ProjectOverview.defaultProps = {
  history: {},
  match: { params: {} },
};

export default ProjectOverview;
