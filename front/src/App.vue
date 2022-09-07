<template>
  <div id="app">
    <ConfirmDialog></ConfirmDialog>

    <template v-if="isLoaded">
      <Menubar :model="menuItemsLoggedIn" v-if="isLoggedIn">
        <template #start
          ><router-link :to="{ name: 'home' }" class="no-underline"
            >StockazIO - {{ backendVersion }}</router-link
          ></template
        >
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

      <div v-if="shouldDisplayCategories" class="grid">
        <div v-if="shouldDisplayCategories" class="col-2 sidebar">
          <div class="sidebar-sticky position-sticky">
            <Tree :value="categories"></Tree>
          </div>
        </div>

        <div role="main" class="col-9">
          <div class="pt-3 pb-2 mb-3">
            <router-view />
          </div>
        </div>
      </div>
      <div v-else class="grid">
        <div class="row">
          <div role="main" class="col-10">
            <router-view />
          </div>
        </div>
      </div>
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
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";

export default {
  setup: () => ({
    oauthStore: useOauthStore(),
    userStore: useUserStore(),
    serverStore: useServerStore(),
    preloadsStore: usePreloadsStore(),
    confirm: useConfirm(),
    toast: useToast(),
  }),
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
      Promise.allSettled([
        this.preloadsStore.preloadSidebar(),
        this.preloadsStore.preloadFootprints(),
        this.preloadsStore.preloadStorages(),
        this.preloadsStore.preloadParametersUnits(),
        this.preloadsStore.preloadPartUnits(),
        this.preloadsStore.preloadManufacturers(),
        this.preloadsStore.preloadDistributors(),
        this.preloadsStore.preloadLabelTemplates(),
        this.preloadsStore.preloadPartParametersPresets(),
      ]).then(() => {
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
          // somehow that won't change in the UI...
          label: this.currentUsername,
          icon: "fa fa-user fa-fw",
          items: [
            { label: "Change password", icon: "fa fa-key fa-fw" },
            {
              label: "Force reload datas",
              icon: "fa fa-refresh",
              command: (event) => {
                this.forceReloadDatas();
              },
            },
            {
              label: "Register URL Handler",
              icon: "fa fa-link",
              command: (event) => {
                this.registerUrlHandler();
              },
            },
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
      currentUsername: (store) => store.currentUsername,
    }),
    ...mapState(useOauthStore, {
      isLoggedIn: (store) => store.loggedIn,
    }),
    ...mapState(usePreloadsStore, {
      categories: (store) => store.categories,
    }),
    shouldDisplayCategories() {
      if (this.currentUser) {
        return true;
      }
      if (
        this.$route.name === "public-parts" ||
        this.$route.name === "public-parts-category-list"
      ) {
        return true;
      }
      return false;
    },
  },
  methods: {
    forceReloadDatas() {
      this.confirm.require({
        message: "Are you sure you want to force reload of all datas ?",
        header: "Please confirm",
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          this.isLoaded = false;

          logger.default.info("Was asked to reload datas");
          this.preloadsStore.setLastUpdate("categories", null);
          this.preloadsStore.setLastUpdate("footprints", null);
          this.preloadsStore.setLastUpdate("storages", null);
          this.preloadsStore.setLastUpdate("parameters_units", null);
          this.preloadsStore.setLastUpdate("part_units", null);
          this.preloadsStore.setLastUpdate("manufacturers", null);
          this.preloadsStore.setLastUpdate("distributors", null);
          this.preloadsStore.setLastUpdate("label_templates", null);
          this.preloadsStore.setLastUpdate("parameters_presets", null);

          Promise.allSettled([
            this.preloadsStore.preloadSidebar(),
            this.preloadsStore.preloadFootprints(),
            this.preloadsStore.preloadStorages(),
            this.preloadsStore.preloadParametersUnits(),
            this.preloadsStore.preloadPartUnits(),
            this.preloadsStore.preloadManufacturers(),
            this.preloadsStore.preloadDistributors(),
            this.preloadsStore.preloadLabelTemplates(),
            this.preloadsStore.preloadPartParametersPresets(),
          ]).then(() => {
            logger.default.info("force preloading finished");
            this.isLoaded = true;
            this.toast.add({
              severity: "success",
              summary: "Reloading datas",
              detail: "Success",
              life: 5000,
            });
          });
        },
        reject: () => {
          return;
        },
      });
    },
    registerUrlHandler() {
      navigator.registerProtocolHandler(
        "web+stockazio",
        `${window.location.origin}/urlhandler?q=%s`,
        "StockazIO handler"
      );
    },
  },
};
</script>

<style lang="scss" src="./App.scss"></style>
