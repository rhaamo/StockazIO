<template>
  <template v-if="isLoaded">
    <header>my super app</header>

    <RouterView />
  </template>
  <template v-else
    ><div id="preloadScreen">
      Preloading in progress.<br /><ProgressSpinner /></div
  ></template>
</template>

<script>
import { useOauthStore } from "@/stores/oauth";
import { useUserStore } from "@/stores/user";
import { useServerStore } from "@/stores/server";
import { usePreloadsStore } from "@/stores/preloads";
import logger from "@/logging";
import { getOrCreateApp } from "@/backend/oauth/oauth.js";
import ProgressSpinner from "primevue/progressspinner";

// TODO move to oauth store
const checkOAuthToken = async (userStore) => {
  return new Promise(async (resolve, reject) => {
    if (userStore.getUserToken) {
      try {
        userStore.loginUser(userStore.getUserToken());
      } catch (e) {
        logger.default.error(e);
      }
    } else {
      logger.default.info("no user token present in cache");
    }
    resolve();
  });
};

export default {
  components: {
    ProgressSpinner,
  },
  setup() {
    const oauthStore = useOauthStore();
    const userStore = useUserStore();
    const serverStore = useServerStore();
    const preloadsStore = usePreloadsStore();
    return { oauthStore, userStore, serverStore, preloadsStore };
  },
  created() {
    logger.default.info("Doing preliminary app initialization...");
    let defaultServerUrl =
      process.env.VUE_APP_SERVER_URL || this.serverStore.defaultUrl;
    logger.default.info("Detected server url:", defaultServerUrl);
    this.serverStore.setServerUrl(defaultServerUrl);

    this.serverStore.fetchSettings();

    Promise.allSettled([
      // Check token and try to log user if found
      checkOAuthToken(this.userStore),
      // Try to get or create oauth2 app and token thingy
      getOrCreateApp(
        this.oauthStore.getClientId,
        this.oauthStore.getClientSecret
      ),
    ]).catch(function (error) {
      logger.default.error("Error while doing initialization", error);
    });
    logger.default.info("Initialization done.");

    if (this.oauthStore.loggedIn) {
      this.preloadsStore.preloadStuff().then(() => {
        console.log("authenticated preloading finished");
        this.isLoaded = true;
      });
    } else {
      // Only preload stuff needed for unauthenticated views
      Promise.allSettled([
        this.preloadsStore.preloadSidebar(),
        this.preloadsStore.preloadFootprints(),
        this.preloadsStore.preloadStorages(),
      ]).then(() => {
        console.log("unauthenticated preloading finished");
        this.isLoaded = true;
      });
    }

    console.log("Initialization finished.");
  },
  mounted() {},
  data() {
    return {
      isLoaded: false,
    };
  },
};
</script>

<style lang="scss" src="./App.scss"></style>
