import React from 'react';
import PropTypes from 'prop-types';
import ProfilePlaceholder from '../../../assets/images/icons/person-with-outline.png';

class CommonHeader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isProject: this.props.isProject,
    };
    this.clickLogo = this.clickLogo.bind(this);
  }

  onKeyPress() {}

  onClickArrowDown() {}

  clickLogo() {
    window.location = 'http://www.dessa.com';
  }

  render() {
    const { isProject } = this.state;
    return (
      <div>
        <div className="foundations-header">
          <div
            tabIndex={0}
            role="button"
            onKeyPress={this.clickLogo}
            onClick={this.clickLogo}
            className="i--icon-dessa-logo"
          />
          <div className="header-link-container">
            { isProject ? <a className="font-bold" href="/projects">Project</a> : <a href="/projects">Project</a> }
            <a href="https://www.atlas.dessa.com/docs">Documentation</a>
            <a href="/support">Support</a>
          </div>
          <div className="header-container-profile">
            <img alt="" src={ProfilePlaceholder} />
            <p>CE User</p>
            { process.env.REACT_APP_SCHEDULER_TYPE !== 'CE'
              && (
                <i
                  onKeyPress={this.onKeyPress}
                  tabIndex={0}
                  role="button"
                  onClick={this.onClickArrowDown}
                  className="i--icon-arrow-down"
                />
              )
            }
          </div>
        </div>
      </div>
    );
  }
}

CommonHeader.propTypes = {
  isProject: PropTypes.bool,
};

CommonHeader.defaultProps = {
  isProject: false,
};

export default CommonHeader;
