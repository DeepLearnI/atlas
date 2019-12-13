import Cookies from 'js-cookie';
import CommonActions from './CommonActions';

const BaseActions = {
  baseURL: process.env.REACT_APP_API_URL,
  baseStagingURL: process.env.REACT_APP_API_STAGING_URL,
  baseApiaryURL: process.env.REACT_APP_APIARY_URL || 'http://private-d03986-iannelladessa.apiary-mock.com/api/v1/',

  get(url) {
    const fullURL = this.baseURL.concat(url);
    const accessToken = CommonActions.getAccessCookie();
    return fetch(fullURL, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((res) => {
        CommonActions.checkStatusResponse(res);
        return res.json();
      })
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log('baseURL get error: ', error);
        return null;
      });
  },

  getFromStaging(url) {
    const fullURL = this.baseStagingURL.concat(url);
    const accessToken = CommonActions.getAccessCookie();
    return fetch(fullURL, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((res) => {
        CommonActions.checkStatusResponse(res);
        return res;
      })
      .then((res) => {
        return res.json();
      })
      .catch((error) => {
        console.log('getFromStaging error: ', error);
        return null;
      });
  },

  async getFromStagingAuth(url, userpass) {
    const fullURL = this.baseStagingURL.concat(url);
    try {
      const fetchResponse = await fetch(fullURL, { headers: { Authorization: `Basic ${userpass}` } });

      const userResponse = await fetchResponse.json();

      if (fetchResponse.status === 200) {
        Cookies.set('atlas_access_token', userResponse.access_token);
        Cookies.set('atlas_refresh_token', userResponse.refresh_token);
      }
      return fetchResponse;
    } catch (error) {
      return error;
    }
  },

  getFromStagingAuthLogout(url) {
    const fullURL = this.baseStagingURL.concat(url);
    const refreshToken = Cookies.get('atlas_refresh_token');
    return fetch(fullURL, {
      headers: {
        Authorization: `Bearer ${refreshToken}`,
      },
    })
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log('getFromStagingAuthLogout error: ', error);
        return error;
      });
  },

  getFromApiary(url) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL)
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log('getFromApiary error: ', error);
        return null;
      });
  },

  post(url, body) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: 'post',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },

  postStaging(url, body) {
    const fullURL = this.baseStagingURL.concat(url);
    const accessToken = CommonActions.getAccessCookie();
    return fetch(fullURL, {
      method: 'post',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((res) => {
        CommonActions.checkStatusResponse(res);
        return res.json();
      })
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },

  postApiary(url, body) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: 'post',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },

  put(url, body) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: 'put',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },

  putStaging(url, body) {
    const fullURL = this.baseStagingURL.concat(url);
    const accessToken = CommonActions.getAccessCookie();
    return fetch(fullURL, {
      method: 'put',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((res) => {
        CommonActions.checkStatusResponse(res);
        return res.json();
      })
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },


  putApiary(url, body) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: 'put',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },

  del(url) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: 'delete',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },

  delStaging(url) {
    const fullURL = this.baseStagingURL.concat(url);
    const accessToken = CommonActions.getAccessCookie();
    return fetch(fullURL, {
      method: 'delete',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((res) => {
        CommonActions.checkStatusResponse(res);
        return res.json();
      })
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },

  delAPIary(url) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: 'delete',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },

  postJSONFile(url, fileName, data) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: 'post',
      body: JSON.stringify({ file: fileName, data }),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.log(error);
        return null;
      });
  },
};

export default BaseActions;
