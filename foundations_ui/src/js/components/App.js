import React, { Component } from 'react';
import {
  BrowserRouter as Router, Route, Switch, Redirect,
} from 'react-router-dom';
import { toast } from 'react-toastify';
import ProjectPage from './ProjectPage/ProjectPage';
import LoginPage from './LoginPage/LoginPage';
import ContactPage from './ContactPage/ContactPage';
import ErrorMessage from './common/ErrorMessage';
import 'react-toastify/dist/ReactToastify.css';
import ProjectOverview from './JobOverviewPage/ProjectOverview';
import JobDetails from './JobOverviewPage/JobDetails';

toast.configure(); // single instance to improve rendering of toast

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <Switch>
            <Route exact path="/login" component={LoginPage} />
            <Route exact path="/projects" component={ProjectPage} />
            <Route exact path="/contact" component={ContactPage} />
            <Redirect exact from="/" to="/projects" />
            <Route
              path="/projects/:projectName/job_listing"
              component={JobDetails}
            />
            <Route
              path="/projects/:projectName/overview"
              component={ProjectOverview}
            />
            <Route render={() => <ErrorMessage errorCode={404} />} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
