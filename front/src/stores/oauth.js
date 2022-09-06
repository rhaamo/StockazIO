import { defineStore } from "pinia";
import logger from "@/logging";
import Axios from "axios";
import { useUserStore } from "@/stores/user";

const REDIRECT_URI = `${window.location.origin}/oauth-callback`;

export const useOauthStore = defineStore("oauth", {
  persist: true,
  state: () => {
    return {
      clientId: false,
      clientSecret: false,
      appToken: false,
      userToken: false,
      loggedIn: false,
    };
  },
  // could also be defined as
  // state: () => ({ count: 0 })
  actions: {
    setClientData(clientId, clientSecret) {
      this.clientId = clientId;
      this.clientSecret = clientSecret;
      logger.default.info("A new OAuth app has been registered");
    },
    setAppToken(token) {
      this.appToken = token;
    },
    setToken(token) {
      this.userToken = token;
    },
    clearToken() {
      this.userToken = false;
      // state.token is userToken with older name, coming from persistent state
      // let's clear it as well, since it is being used as a fallback of state.userToken
      delete this.token;
    },
    setLoggedIn(value) {
      this.loggedIn = value;
    },
    clearTokens() {
      this.clientId = false;
      this.clientSecret = false;
      this.appToken = false;
      this.userToken = false;
    },
    // Get the clientId and clientSecret if any or generate a new one
    getOrCreateApp(cid, csecret) {
      logger.default.debug("getOrCreateApp called");
      if (cid && csecret) {
        logger.default.info("We are using already known OAuth App infos");
        return Promise.resolve({ cid, csecret });
      }

      // TODO move to api.service.js
      return Axios.post("/oauth/apps/", {
        name: `stockazio_front_${new Date().toISOString()}`,
        redirect_uris: REDIRECT_URI,
        scopes:
          "read write read:check_oauth_token read:app read:parts write:parts read:projects write:projects",
      })
        .then((app) => ({
          clientId: app.data.client_id,
          clientSecret: app.data.client_secret,
        }))
        .then((app) => this.setClientData(app) || app);
    },
    // Get a token through password grant type
    getTokenWithCredentials(cid, csecret, uname, upass) {
      logger.default.debug("getTokenWithCredentials called");
      // TODO move to api.service.js
      return Axios.post("/oauth/token/", {
        client_id: cid,
        client_secret: csecret,
        grant_type: "password",
        scope:
          "read write read:check_oauth_token read:app read:parts write:parts read:projects write:projects",
        username: uname,
        password: upass,
      });
    },
    // Revoke a token
    revokeToken(app, token) {
      logger.default.debug("revokeToken called");
      // TODO move to api.service.js
      return Axios.post("/oauth/revoke/", {
        client_id: app.clientId,
        client_secret: app.clientSecret,
        token: token,
      });
    },
  },
  getters: {
    getToken(state) {
      // state.token is userToken with older name, coming from persistent state
      // added here for smoother transition, otherwise user will be logged out
      return state.userToken || state.token || state.appToken;
    },
    getUserToken(state) {
      // state.token is userToken with older name, coming from persistent state
      // added here for smoother transition, otherwise user will be logged out
      return state.userToken || state.token;
    },
    getClientId(state) {
      return state.clientId;
    },
    getClientSecret(state) {
      return state.clientSecret;
    },
    getLoggedIn(state) {
      return state.loggedIn;
    },
  },
});
