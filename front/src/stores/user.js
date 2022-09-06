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
          oauthStore.userToken.accessToken,
          oauthStore.clientId.clientId,
          oauthStore.clientId.clientSecret
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
      await apiService.verifyCredentials().then((result) => {
        logger.default.info("credentials validated");
        oauthStore.setLoggedIn(true);
        this.currentUser = result.data.user;
      });
    },
    async checkOauthToken() {
      return new Promise(async (resolve, reject) => {
        if (this.getUserToken) {
          try {
            this.loginUser(this.getUserToken());
          } catch (e) {
            logger.default.error(e);
          }
        } else {
          logger.default.info("no user token present in cache");
        }
        resolve();
      });
    },
  },
});
