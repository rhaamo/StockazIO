<template>
  <div id="app">
    <ConfirmDialog></ConfirmDialog>
    <Toast />
    <DynamicDialog />

    <template v-if="isLoaded && !cannotLoad">
      <Menubar :model="menuItemsLoggedIn" v-if="isLoggedIn">
        <template #start
          ><router-link :to="{ name: 'home' }" class="no-underline"
            >StockazIO</router-link
          ></template
        >
        <template #end>
          <form role="search" @submit.prevent="doSearch">
            <div class="p-inputgroup">
              <InputText v-model="searchTerm" placeholder="Keyword" />
              <PvButton type="submit" label="Search" />
            </div>
          </form>
        </template>
      </Menubar>
      <Menubar :model="menuItemsLoggedOut" v-else>
        <template #start
          ><router-link :to="{ name: 'home' }" class="no-underline"
            >StockazIO</router-link
          ></template
        >
        <template #end> </template>
      </Menubar>

      <div v-if="shouldDisplayCategories" class="grid">
        <div v-if="shouldDisplayCategories" class="col-2 sidebar mt-3">
          <div class="sidebar-sticky position-sticky">
            <CategoryTree :tree-data="categories" />
          </div>
        </div>

        <div role="main" class="col-10">
          <div class="pt-3 pb-2 mb-3 ml-1">
            <router-view />
          </div>
        </div>
      </div>
      <div v-else class="grid">
        <div role="main" class="col-12">
          <router-view />
        </div>
      </div>
    </template>

    <template v-if="!isLoaded && !cannotLoad">
      <div id="preloadScreen">
        Preloading in progress.<br /><ProgressSpinner />
      </div>
    </template>

    <template v-if="!isLoaded && cannotLoad">
      <div id="preloadScreen">
        An error occured and the application cannot load.
      </div>
    </template>
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
import CategoryTree from "@/components/categories/tree.vue";

export default {
  setup: () => ({
    oauthStore: useOauthStore(),
    userStore: useUserStore(),
    serverStore: useServerStore(),
    preloadsStore: usePreloadsStore(),
    confirm: useConfirm(),
    toast: useToast(),
  }),
  components: {
    CategoryTree,
  },
  created() {
    logger.default.info("Doing preliminary app initialization...");
    let defaultServerUrl =
      process.env.VUE_APP_SERVER_URL || this.serverStore.defaultUrl;
    logger.default.info("Detected server url:", defaultServerUrl);
    this.serverStore.setServerUrl(defaultServerUrl);

    this.serverStore
      .fetchSettings()
      .then(() => {
        Promise.allSettled([
          // Check token and try to log user if found
          this.userStore.checkOauthToken(),
          // Try to get or create oauth2 app and token thingy
          this.oauthStore.getOrCreateApp(
            this.oauthStore.getClientId,
            this.oauthStore.getClientSecret
          ),
        ])
          .then(() => {
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
              ])
                .then(() => {
                  logger.default.info("authenticated preloading finished");
                  this.isLoaded = true;
                  logger.default.info("Initialization finished.");
                })
                .catch(() => {
                  logger.default.error("Cannot preload stuff");
                });
            } else {
              // Only preload stuff needed for unauthenticated views
              Promise.allSettled([
                this.preloadsStore.preloadSidebar(),
                this.preloadsStore.preloadFootprints(),
                this.preloadsStore.preloadStorages(),
              ]).then(() => {
                logger.default.info("unauthenticated preloading finished");
                this.isLoaded = true;
                logger.default.info("Initialization finished.");
              });
            }
          })
          .catch(function (error) {
            logger.default.error("Error while doing initialization", error);
          });
      })
      .catch((err) => {
        logger.default.error("Cannot load settings.");
        this.isLoaded = false;
        this.cannotLoad = true;
        return;
      });
  },
  mounted() {},
  data() {
    return {
      isLoaded: false,
      cannotLoad: false,
      searchTerm: "",
      menuItemsLoggedIn: [
        { separator: true },
        {
          label: "Edit",
          icon: "fa fa-cogs fa-fw",
          items: [
            {
              label: "Footprints",
              icon: "fa fa-paw fa-fw",
              to: { name: "footprints-list" },
            },
            {
              label: "Manufacturers",
              icon: "fa fa-home fa-fw",
              to: { name: "manufacturers-list" },
            },
            {
              label: "Distributors",
              icon: "fa fa-car fa-fw",
              to: { name: "distributors-list" },
            },
            {
              label: "Storage",
              icon: "fa fa-archive fa-fw",
              to: { name: "storages-list" },
            },
            {
              label: "Parts units",
              icon: "fa fa-cogs fa-fw",
              to: { name: "part-units-list" },
            },
            {
              label: "Parameters Units",
              icon: "fa fa-cogs fa-fw",
              to: { name: "parameters-units-list" },
            },
            {
              label: "Part Parameters Presets",
              icon: "fa fa-list fa-fw",
              to: { name: "parameters-presets-list" },
            },
            {
              label: "Label Templates",
              icon: "fa fa-file-text fa-fw",
              to: { name: "label-templates-list" },
            },
            {
              label: "Categories",
              icon: "fa fa-tree fa-fw",
              to: { name: "categories-list" },
            },
          ],
        },
        {
          label: "View",
          icon: "fa fa-list fa-fw",
          items: [
            {
              label: "Informations",
              icon: "fa fa-cogs fa-fw",
              to: { name: "view-infos" },
            },
            {
              label: "Storage tree",
              icon: "fa fa-list-alt fa-fw",
              to: { name: "view-storage-tree" },
            },
            {
              label: "Public parts",
              icon: "fa fa-list-alt fa-fw",
              to: { name: "public-parts" },
            },
          ],
        },
        {
          label: "Tools",
          icon: "fa fa-tasks fa-fw",
          items: [
            {
              label: "Orders importer",
              icon: "fa fa-shopping-cart fa-fw",
              to: { name: "orders-importer" },
            },
            {
              label: "Projects",
              icon: "fa fa-list-ul fa-fw",
              to: { name: "projects-list" },
            },
          ],
        },
        { separator: true },
        {
          label: "Add part",
          icon: "fa fa-plus fa-fw",
          to: { name: "parts-new" },
        },
        {
          label: "Quick add part",
          icon: "fa fa-fast-forward fa-fw",
          to: { name: "parts-quick-new" },
        },
        { separator: true },
        {
          // somehow that won't change in the UI...
          label: this.currentUsername,
          icon: "fa fa-user fa-fw",
          items: [
            {
              label: "Change password",
              icon: "fa fa-key fa-fw",
              to: { name: "password-reset-request" },
            },
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
    doSearch() {
      let search = this.searchTerm;
      this.searchTerm = "";

      if (search.startsWith("stockazio://storageLocation/")) {
        // old url handler (location)
        let str = search.split("/");
        let uuid = str[str.length - 1];
        this.$router
          .replace({ name: "parts-list", query: { storage_uuid: uuid } })
          .catch(() => {});
      } else if (search.startsWith("web+stockazio:storageLocation,")) {
        // new url handler (location)
        let str = search.split(",");
        let uuid = str[str.length - 1];
        this.$router
          .replace({ name: "parts-list", query: { storage_uuid: uuid } })
          .catch(() => {});
      } else if (search.startsWith("stockazio://part/")) {
        // old url handler (part)
        let str = search.split("/");
        let uuid = str[str.length - 1];
        this.$router
          .replace({ name: "parts-details", params: { partId: uuid } })
          .catch(() => {});
      } else if (search.startsWith("web+stockazio:part,")) {
        // new url handler (part)
        let str = search.split(",");
        let uuid = str[str.length - 1];
        this.$router
          .replace({ name: "parts-details", params: { partId: uuid } })
          .catch(() => {});
      } else {
        // keyword search
        this.$router
          .replace({ name: "parts-list", query: { q: search } })
          .catch(() => {});
      }
    },
  },
};
</script>

<style lang="scss" src="./App.scss"></style>
