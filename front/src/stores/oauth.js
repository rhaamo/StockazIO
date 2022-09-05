import { defineStore } from "pinia";
import logger from "@/logging";

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
