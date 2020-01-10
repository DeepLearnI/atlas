import React from 'react';
import ReactDOM from 'react-dom';
import ProjectPage from '../../js/components/ProjectPage/ProjectPage';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router-dom';
import configureTests from '../setupTests';
import LoginPage from '../../js/components/LoginPage/LoginPage';

configureTests();

/*it('Shallow Renders ProjectPage', () => {
  const wrapper = shallow(<ProjectPage/>);
  expect(wrapper).toMatchSnapshot();
});*/

it('Calls Get All Projects', async () => {
  <MemoryRouter>
    const wrapper = mount(<ProjectPage/>); 
    const preState = wrapper.state();
    await wrapper.instance().getAllProjects();
    const postState = wrapper.state();
    expect(preState.isLoaded === false);
    expect(postState.isLoaded === true);
  </MemoryRouter>
});

// Assumes your API has projects
it('Has at least One Project', async () => {
  <MemoryRouter>
    const wrapper = mount(<ProjectPage/>); 
    const preState = wrapper.state();
    await wrapper.instance().getAllProjects();
    const postState = wrapper.state();
    expect(preState.projects.length === 0);
    expect(postState.projects.length > 0);
  </MemoryRouter>
});
