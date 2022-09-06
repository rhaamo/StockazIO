<template>
  <div id="app">
    <template v-if="isLoaded">
      <Menubar :model="menuItemsLoggedIn" v-if="isLoggedIn">
        <template #start>StockazIO - {{ backendVersion }}</template>
        <template #end>
          <div class="p-inputgroup">
            <InputText placeholder="Keyword" />
            <Button label="Search" />
          </div>
        </template>
      </Menubar>
      <Menubar :model="menuItemsLoggedOut" v-else>
        <template #start>StockazIO - {{ backendVersion }}</template>
        <template #end> </template>
      </Menubar>

      <RouterView />
    </template>
    <template v-else
      ><div id="preloadScreen">
        Preloading in progress.<br /><ProgressSpinner /></div
    ></template>
  </div>
</template>

<script>
import { useOauthStore } from "@/stores/oauth";
import { useUserStore } from "@/stores/user";
import { useServerStore } from "@/stores/server";
import { usePreloadsStore } from "@/stores/preloads";
import logger from "@/logging";
import { mapState } from "pinia";

export default {
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
      this.userStore.checkOauthToken(),
      // Try to get or create oauth2 app and token thingy
      this.oauthStore.getOrCreateApp(
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
      menuItemsLoggedIn: [
        { separator: true },
        { label: "Edit", icon: "fa fa-cogs fa-fw", items: [] },
        { label: "View", icon: "fa fa-list fa-fw", items: [] },
        { label: "Tools", icon: "fa fa-tasks fa-fw", items: [] },
        { separator: true },
        { label: "Projects", icon: "fa fa-list-ul fa-fw" },
        { label: "Add part", icon: "fa fa-plus fa-fw" },
        { label: "Quick add part", icon: "fa fa-fast-forward fa-fw" },
        { separator: true },
        {
          label: this.currentUser ? this.currentUser.username : ":3",
          icon: "fa fa-user fa-fw",
          items: [
            { label: "Change password", icon: "fa fa-key fa-fw" },
            { label: "Force reload datas", icon: "fa fa-refresh" },
            { label: "Register URL Handler", icon: "fa fa-link" },
            { separator: true },
            {
              label: "Logout",
              icon: "fa fa-sign-out fa-fw",
              command: (event) => {
                this.userStore.logout().then(() => {
                  this.$router.replace({ name: "login_form" });
                });
              },
            },
          ],
        },
      ],
      menuItemsLoggedOut: [
        { separator: true },
        { label: "Login", to: { name: "login_form" } },
        { label: "Public parts list", to: { name: "public-parts" } },
        { label: "About", to: { name: "about" } },
      ],
    };
  },
  computed: {
    ...mapState(useServerStore, {
      backendVersion: (store) => store.settings.backendVersion,
    }),
    ...mapState(useUserStore, {
      currentUser: (store) => store.currentUser,
    }),
    ...mapState(useOauthStore, {
      isLoggedIn: (store) => store.loggedIn,
    }),
  },
};
</script>

<style lang="scss" src="./App.scss"></style>
