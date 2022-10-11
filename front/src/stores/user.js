import logger from "@/logging";
import apiService from "@/services/api/api.service";
import { useOauthStore } from "@/stores/oauth";
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  persist: false,
  state: () => ({
    currentUser: false,
    settings: {},
  }),
  getters: {
    getSettings() {
      return this.settings;
    },
    currentUsername() {
      return this.currentUser ? this.currentUser.username : false;
    },
  },
  actions: {
    setCurrentUser(user) {
      this.currentUser = user;
    },
    async logout() {
      const oauthStore = useOauthStore();

      logger.default.info("logging out");

      await apiService
        .oauthRevoke(
          oauthStore.userToken.access_token,
          oauthStore.clientId,
          oauthStore.clientSecret
        )
        .then(() => {
          this.currentUser = null;
          oauthStore.setLoggedIn(false);
          oauthStore.clearTokens();
        });
    },
    async login(access_token) {
      const oauthStore = useOauthStore();

      // Store token in store
      oauthStore.setToken(access_token);

      // Check the token validity
      await apiService
        .verifyCredentials()
        .then((result) => {
          logger.default.info("login: credentials validated");
          oauthStore.setLoggedIn(true);
          this.currentUser = result.data.user;
        })
        .catch((error) => {
          logger.default.error(
            "login: cannot verify credentials",
            error.message
          );
          oauthStore.setLoggedIn(false);
          this.currentUser = {};
        });
    },
    loginUser() {
      return new Promise((resolve, reject) => {
        const oauthStore = useOauthStore();
        logger.default.info("loginUser: verifying credentials");
        apiService
          .verifyCredentials()
          .then((result) => {
            logger.default.info("loginUser: credentials validated");
            oauthStore.setLoggedIn(true);
            this.currentUser = result.data.user;
            resolve();
          })
          .catch((error) => {
            logger.default.error(
              "loginUser: cannot verify credentials",
              error.message
            );
            oauthStore.setLoggedIn(false);
            this.currentUser = {};
            reject(error);
          });
      });
    },
    checkOauthToken() {
      // eslint-disable-next-line no-async-promise-executor
      return new Promise(async (resolve, reject) => {
        const oauthStore = useOauthStore();
        if (oauthStore.getUserToken) {
          logger.default.info("we have an user token present in cache");
          try {
            await this.loginUser().then(() => {
              resolve();
            });
          } catch (e) {
            logger.default.error(e);
            reject(e);
          }
        } else {
          logger.default.info("no user token present in cache");
          resolve();
        }
      });
    },
  },
});
