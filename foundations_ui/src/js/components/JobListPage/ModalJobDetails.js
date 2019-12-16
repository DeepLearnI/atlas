/* eslint-disable react/jsx-closing-bracket-location */
/* eslint-disable react/jsx-closing-tag-location */
import React from 'react';
import { Modal, ModalBody } from 'reactstrap';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { toast } from 'react-toastify';
import BaseActions from '../../actions/BaseActions';
import Tag from '../common/Tag';
import ArtifactsTable from './ArtifactsTable';
import Logs from './Logs';
import ImageViewer from './job-sidebar/ImageViewer';
import AudioPlayer from './job-sidebar/AudioPlayer';
import ArtifactViewer from './job-sidebar/ArtifactViewer';

class ModalJobDetails extends React.Component {
  constructor(props) {
    super(props);

    const { job, reloadJobTable } = this.props;

    this.state = {
      tags: [],
      tab: 'logs',
      newTagKey: '',
      newTagValue: '',
      timerId: -1,
      addNewTagVisible: false,
      job: job,
      selectedArtifact: {},
      reloadJobTable: reloadJobTable,
    };

    this.onClickRemoveTag = this.onClickRemoveTag.bind(this);
    this.onClickLogs = this.onClickLogs.bind(this);
    this.onClickArtifacts = this.onClickArtifacts.bind(this);
    this.onChangeTagKey = this.onChangeTagKey.bind(this);
    this.onChangeTagValue = this.onChangeTagValue.bind(this);
    this.onClickShowAddTag = this.onClickShowAddTag.bind(this);
    this.onClickAddNewTag = this.onClickAddNewTag.bind(this);
    this.onClickCancelAddNewTag = this.onClickCancelAddNewTag.bind(this);
    this.onClickRemoveTag = this.onClickRemoveTag.bind(this);
    this.onClickArtifact = this.onClickArtifact.bind(this);
    this.onClickAtlasDocs = this.onClickAtlasDocs.bind(this);
    this.onTagKeyPress = this.onTagKeyPress.bind(this);
  }

  reload() {
    const { location } = this.props;
    const { job } = this.state;
    const { projectName } = this.props.match.params;
    const selectedProjectName = location.state && location.state.project ? location.state.project.name : projectName;
    BaseActions.getFromStaging(`projects/${selectedProjectName}/job_listing`)
      .then(result => {
        const filteredJob = result.jobs.find(item => item.job_id === job.job_id);
        let newTags = [];
        if (filteredJob.tags) {
          if (Array.isArray(filteredJob.tags)) {
            newTags = filteredJob.tags;
          } else {
            newTags = Object.keys(filteredJob.tags);
          }
        }
        this.setState({
          addNewTagVisible: false,
          tags: newTags,
          job: filteredJob,
        });
      });
  }

  componentDidMount() {
    this.reload();
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
    this.state.reloadJobTable();
  }

  onToggleModal() {
    const { onToggle } = this.props;
    const { job } = this.state;
    onToggle(job);
  }

  onClickShowAddTag() {
    this.setState({
      addNewTagVisible: true,
    });
  }

  onClickRemoveTag(tag) {
    const { job } = this.state;
    const { location } = this.props;
    const { projectName } = this.props.match.params;
    const selectedProjectName = location.state.project ? location.state.project.name : projectName;
    BaseActions.delStaging(`projects/${selectedProjectName}/job_listing/${job.job_id}/tags/${tag}`)
      .then(result => {
        this.reload();
        this.state.reloadJobTable();
      });
  }

  notifiedCopy(e) {
    e.stopPropagation();
    toast.info('Job ID successfully copied', {
      autoClose: 1500,
      draggable: false,
    });
  }

  onKeyDown() { }

  onClickLogs() {
    this.setState({
      tab: 'logs',
    });
  }

  onClickArtifacts() {
    this.setState({
      tab: 'artifacts',
    });
  }

  onChangeTagKey(e) {
    this.setState({
      newTagKey: e.target.value,
    });
  }

  onTagKeyPress(e) {
    if (e.key === 'Enter') {
      this.onClickAddNewTag();
    }
  }

  onChangeTagValue(e) {
    this.setState({
      newTagValue: e.target.value,
    });
  }

  onClickAddNewTag() {
    const { newTagKey, newTagValue, job } = this.state;
    const { location } = this.props;
    const { projectName } = this.props.match.params;
    const selectedProjectName = location.state.project ? location.state.project.name : projectName;

    const body = {
      tag: {
        key: newTagKey,
        value: newTagValue,
      },
    };

    BaseActions.postStaging(`projects/${selectedProjectName}/job_listing/${job.job_id}/tags`, body)
      .then(result => {
        this.reload();
        this.state.reloadJobTable();
      });
  }

  onClickCancelAddNewTag() {
    this.setState({
      addNewTagVisible: false,
    });
  }

  onClickArtifact(newArtifact) {
    this.setState({ selectedArtifact: newArtifact });
  }

  onClickAtlasDocs() {
    window.location = 'https://www.atlas.dessa.com/docs';
  }

  render() {
    const { visible, onToggle } = this.props;
    const {
      tags,
      tab,
      addNewTagVisible,
      job,
      selectedArtifact,
    } = this.state;

    const selectViewer = artifact => {
      switch (artifact.artifact_type) {
        case 'image':
          return <ImageViewer image={artifact.uri} />;
        case 'audio':
          return <AudioPlayer url={artifact.uri} />;
        default:
          return (
            <p className="media">
              This type of artifact is not viewable. Download the artifact to be able to view it.
              <span>
                Check out the <span
                  role="button"
                  onKeyPress={this.onClickAtlasDocs}
                  tabIndex={0}
                  onClick={this.onClickAtlasDocs}>Atlas Documentation</span> to learn about saving artifacts.
              </span>
            </p>
          );
      }
    };

    return (
      <Modal
        isOpen={visible}
        toggle={onToggle}
        className="modal-job-details"
      >
        <ModalBody>
          <div className="contanier-main">
            <div className="container-title">
              <p className="label-id">Details For Job</p>
              <div className="container-id">
                <p className="text-id">{job.job_id}</p>
                <CopyToClipboard text={job.job_id}>
                  <span
                    onClick={this.notifiedCopy}
                    className="i--icon-copy"
                    role="presentation"
                  />
                </CopyToClipboard>
              </div>
              <div
                className="close"
                onClick={onToggle}
                role="button"
                aria-label="Close"
                onKeyDown={this.onKeyDown}
                tabIndex={0}
              />
            </div>
            <div className="container-tags" data-class="job-details-tags">
              {tags.map(tag => {
                return <Tag key={tag} value={tag} removeVisible removeTag={() => this.onClickRemoveTag(tag)} />;
              })}
              <div
                className="button-add"
                onClick={this.onClickShowAddTag}
                role="button"
                aria-label="Add Tag"
                onKeyDown={this.onKeyDown}
                tabIndex={0}
              >
                +
              </div>
              {addNewTagVisible === true
                && (
                  <div className="container-add-new-tag">
                    <input onChange={this.onChangeTagKey} onKeyPress={this.onTagKeyPress} placeholder="Tag Value" />
                    {/* <input onChange={this.onChangeTagValue} placeholder="Tag Value" /> */}
                    <button type="button" onClick={this.onClickAddNewTag}>SAVE</button>
                    <button type="button" onClick={this.onClickCancelAddNewTag}>CANCEL</button>
                  </div>
                )}
            </div>
            <div className="container-tabs">
              <div>
                <h3
                  className={tab === 'logs' ? 'active' : ''}
                  onClick={this.onClickLogs}
                  onKeyDown={this.onKeyDown}
                >
                  Logs
                </h3>
                <h3
                  className={tab === 'artifacts' ? 'active' : ''}
                  onClick={this.onClickArtifacts}
                  onKeyDown={this.onKeyDown}
                  data-class="artifacts-tab-button"
                >
                  Artifacts
                </h3>
              </div>
            </div>
            {tab === 'logs' && <Logs job={job} {...this.props} />}
            {tab === 'artifacts' && (
              <div className="container-artifacts">
                <div className="image-artifacts">
                  <ArtifactViewer jobId={job.job_id}>
                    {selectViewer(selectedArtifact)}
                  </ArtifactViewer>
                </div>
                <ArtifactsTable onClickArtifact={this.onClickArtifact} job={job} {...this.props} />
              </div>
            )}
          </div>
        </ModalBody>
      </Modal>
    );
  }
}


ModalJobDetails.propTypes = {
  job: PropTypes.object,
  visible: PropTypes.bool,
  onToggle: PropTypes.func,
  location: PropTypes.object,
  match: PropTypes.object,
  reloadJobTable: PropTypes.func,
};

ModalJobDetails.defaultProps = {
  job: {},
  visible: false,
  onToggle: () => null,
  location: { state: {} },
  match: { params: {} },
  reloadJobTable: () => null,
};

export default withRouter(ModalJobDetails);
