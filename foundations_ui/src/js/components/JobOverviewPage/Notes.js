import React from 'react';
import moment from 'moment';
import PropTypes from 'prop-types';
import Cookies from 'js-cookie';
import jwt from 'jwt-decode';
import ProfilePlaceholder from '../../../assets/images/icons/person-with-outline.png';
import BaseActions from '../../actions/BaseActions';
import NoCommentsImage from '../../../assets/svgs/empty-notes.svg';

class Notes extends React.Component {
  constructor(props) {
    super(props);

    this.onChangeMessage = this.onChangeMessage.bind(this);
    this.onClickAddNote = this.onClickAddNote.bind(this);
    this.reload = this.reload.bind(this);

    this.state = {
      notes: [],
      message: '',
      timerId: -1,
    };
  }

  reload() {
    const { location } = this.props;
    const { projectName } = this.props.match.params;
    const selectedProjectName = location.state && location.state.project ? location.state.project.name : projectName;
    BaseActions.getFromStaging(`projects/${selectedProjectName}/note_listing`).then(result => {
      if (result) {
        result.sort((a, b) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          return dateB - dateA;
        });
        this.setState({
          notes: result,
        });
      }
    });
  }

  componentDidMount() {
    this.reload();
    /* const value = setInterval(() => {
      this.reload();
    }, 4000);

    this.setState({
      timerId: value,
    }); */
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  onChangeMessage(e) {
    this.setState({
      message: e.target.value,
    });
  }

  onClickAddNote() {
    const { message } = this.state;
    const { location } = this.props;
    const { projectName } = this.props.match.params;
    const selectedProjectName = location.state.project ? location.state.project.name : projectName;

    const atlasAccessToken = Cookies.get('atlas_access_token');
    const decodeToken = jwt(atlasAccessToken);
    const tokenUserID = decodeToken.sub;

    const body = {
      message: message,
      author: tokenUserID,
    };

    BaseActions.postStaging(`projects/${projectName}/note_listing`, body).then(() => {
      this.setState({
        message: '',
      }, () => {
        this.reload();
      });
    });
  }

  render() {
    const { notes, message } = this.state;
    return (
      <div className="container-notes">
        <div className="notes section-container">
          <h3 className="section-title">Comments</h3>
          <div className="notes-textarea">
            <textarea placeholder="Add a comment..." value={message} onChange={this.onChangeMessage} />
            <button
              disabled={message === ''}
              className={message === '' ? 'disabled' : ''}
              style={message === '' ? {} : { cursor: 'pointer' }}
              type="button"
              onClick={this.onClickAddNote}
            >
              Add Note
            </button>
          </div>
          { notes.length === 0 && (
            <div className="no-comments-block">
              <h3>No comments yet, try adding one!</h3>
              <img alt="" className="no-comments-image" src={NoCommentsImage} />
            </div>
          )}
          { notes.length !== 0 && notes.map(note => {
            return (
              <div key={note.date} className="notes-blocks">
                <div className="container-note-profile">
                  <img alt="" src={ProfilePlaceholder} />
                  <p><span className="font-bold">{note.author} </span>
                    <span>{moment(note.date).format('MMMM Do, YYYY').toString()}</span>
                  </p>
                </div>
                <p>{note.message}</p>
              </div>
            );
          })}
        </div>
      </div>

    );
  }
}

Notes.propTypes = {
  location: PropTypes.object,
  match: PropTypes.object,
};

Notes.defaultProps = {
  location: { state: {} },
  match: { params: {} },
};

export default Notes;
