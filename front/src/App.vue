<template>
  <div id="app">
    <ConfirmPopup></ConfirmPopup>
    <ConfirmDialog group="dialog"></ConfirmDialog>
    <Toast />
    <DynamicDialog />

    <template v-if="isLoaded && !cannotLoad">
      <Menubar v-if="isLoggedIn" :model="menuItemsLoggedIn">
        <template #start><router-link :to="{ name: 'home' }" class="no-underline">StockazIO</router-link></template>
        <template #end>
          <form role="search" @submit.prevent="doSearch">
            <div class="p-inputgroup">
              <InputText ref="searchInput" v-model="searchTerm" placeholder="Keyword" class="mr-2" @focus="$event.target.select()" />
              <PvButton type="submit" label="Search" />
            </div>
          </form>
        </template>
      </Menubar>
      <Menubar v-else :model="menuItemsLoggedOut">
        <template #start><router-link :to="{ name: 'home' }" class="no-underline">StockazIO</router-link></template>
        <template #end> </template>
      </Menubar>

      <div v-if="shouldDisplayCategories" class="grid">
        <div v-if="shouldDisplayCategories" class="col-2 sidebar mt-3">
          <div class="sidebar-sticky position-sticky">
            <Tree
              :value="choicesCategory"
              filter
              v-model:expandedKeys="expandedCategoryKeys"
              autoSize
              lazy
              selectionMode="single"
              @nodeSelect="changeCategory"
              v-model:selectionKeys="selectedCategory">
            </Tree>
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
      <div id="preloadScreen">Preloading in progress.<br /><ProgressSpinner /></div>
    </template>

    <template v-if="!isLoaded && cannotLoad">
      <div id="preloadScreen">An error occured and the application cannot load.</div>
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
import { useRoute } from "vue-router";
import { ConfirmDialog } from "primevue";

export default {
  components: {},
  setup: () => ({
    oauthStore: useOauthStore(),
    userStore: useUserStore(),
    serverStore: useServerStore(),
    preloadsStore: usePreloadsStore(),
    confirm: useConfirm(),
    toast: useToast(),
    route: useRoute(),
  }),
  data() {
    return {
      isLoaded: false,
      cannotLoad: false,
      searchTerm: "",
      menuItemsLoggedIn: [
        { separator: true },
        {
          label: "Edit",
          icon: "pi pi-cog",
          items: [
            {
              label: "Footprints",
              icon: "pi pi-microchip",
              command: () => {
                this.$router.push({ name: "footprints-list" });
              },
            },
            {
              label: "Manufacturers",
              icon: "pi pi-building",
              command: () => {
                this.$router.push({ name: "manufacturers-list" });
              },
            },
            {
              label: "Distributors",
              icon: "pi pi-truck",
              command: () => {
                this.$router.push({ name: "distributors-list" });
              },
            },
            {
              label: "Storage",
              icon: "pi pi-box",
              command: () => {
                this.$router.push({ name: "storages-list" });
              },
            },
            {
              label: "Parts units",
              icon: "pi pi-cog",
              command: () => {
                this.$router.push({ name: "part-units-list" });
              },
            },
            {
              label: "Parameters Units",
              icon: "pi pi-cog",
              command: () => {
                this.$router.push({ name: "parameters-units-list" });
              },
            },
            {
              label: "Part Parameters Presets",
              icon: "pi pi-list",
              command: () => {
                this.$router.push({ name: "parameters-presets-list" });
              },
            },
            {
              label: "Label Templates",
              icon: "pi pi-tags",
              command: () => {
                this.$router.push({ name: "label-templates-list" });
              },
            },
            {
              label: "Categories",
              icon: "pi pi-sitemap",
              command: () => {
                this.$router.push({ name: "categories-list" });
              },
            },
          ],
        },
        {
          label: "View",
          icon: "pi pi-list",
          items: [
            {
              label: "Informations",
              icon: "pi pi-question",
              command: () => {
                this.$router.push({ name: "view-infos" });
              },
            },
            {
              label: "Storage tree",
              icon: "pi pi-list",
              command: () => {
                this.$router.push({ name: "view-storage-tree" });
              },
            },
            {
              label: "Public parts",
              icon: "pi pi-list",
              command: () => {
                this.$router.push({ name: "public-parts" });
              },
            },
          ],
        },
        {
          label: "Tools",
          icon: "pi pi-hammer",
          items: [
            {
              label: "Orders importer",
              icon: "pi pi-shopping-cart",
              command: () => {
                this.$router.push({ name: "orders-importer" });
              },
            },
            {
              label: "Projects",
              icon: "pi pi-list",
              command: () => {
                this.$router.push({ name: "projects-list" });
              },
            },
          ],
        },
        { separator: true },
        {
          label: "Add part",
          icon: "pi pi-plus",
          command: () => {
            this.$router.push({ name: "parts-new" });
          },
        },
        {
          label: "Quick add part",
          icon: "pi pi-fast-forward",
          command: () => {
            this.$router.push({ name: "parts-quick-new" });
          },
        },
        { separator: true },
        {
          // somehow that won't change in the UI...
          label: this.currentUsername,
          icon: "pi pi-user",
          items: [
            {
              label: "Change password",
              icon: "pi pi-key",
              command: () => {
                this.$router.push({ name: "password-reset-request" });
              },
            },
            {
              label: "Force reload datas",
              icon: "pi pi-refresh",
              command: (event) => {
                this.forceReloadDatas();
              },
            },
            {
              label: "Register URL Handler",
              icon: "pi pi-link",
              command: (event) => {
                this.registerUrlHandler();
              },
            },
            { separator: true },
            {
              label: "Logout",
              icon: "pi pi-sign-out",
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
        {
          label: "Login",
          command: () => {
            this.$router.push({ name: "login_form" });
          },
        },
        {
          label: "Public parts list",
          command: () => {
            this.$router.push({ name: "public-parts" });
          },
        },
        {
          label: "About",
          command: () => {
            this.$router.push({ name: "about" });
          },
        },
      ],
      expandedCategoryKeys: {},
      selectedCategory: null,
    };
  },
  created() {
    logger.default.info("Doing preliminary app initialization...");
    let defaultServerUrl = process.env.VUE_APP_SERVER_URL || this.serverStore.defaultUrl;
    logger.default.info("Detected server url:", defaultServerUrl);
    this.serverStore.setServerUrl(defaultServerUrl);

    this.serverStore
      .fetchSettings()
      .then(() => {
        Promise.allSettled([
          // Check token and try to log user if found
          this.userStore.checkOauthToken(),
          // Try to get or create oauth2 app and token thingy
          this.oauthStore.getOrCreateApp(this.oauthStore.getClientId, this.oauthStore.getClientSecret),
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
  mounted() {
    this.expandAllCategoryChoices();
    // Duplicate to avoid fucking up the store
    this.selectedCategory = { ...this.currentCategory };
    if (this.route.query.q) {
      this.searchTerm = this.$route.query.q;
    }
  },
  computed: {
    ...mapState(useServerStore, {
      backendVersion: (store) => store.settings.backendVersion,
      parts_uncategorized_count: (store) => (typeof store.parts_uncategorized_count == "number" ? store.parts_uncategorized_count : "n/a"),
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
      currentCategory: (store) => store.currentCategory,
    }),
    shouldDisplayCategories() {
      if (this.currentUser) {
        return true;
      }
      if (this.$route.name === "public-parts" || this.$route.name === "public-parts-category-list") {
        return true;
      }
      return false;
    },
    categoriesRouteName() {
      return this.currentUser ? "parts-category-list" : "public-parts-category-list";
    },
    choicesCategory() {
      const cb = (e) => {
        // base object
        let obj = {
          key: e.id,
          label: `${e.name} (${e.parts_count})`,
          icon: `pi pi-folder`,
          parts_count: e.parts_count,
        };
        obj["children"] = e.children.map(cb);
        if (e.children.length) {
          obj["leaf"] = true;
        }
        if (e.parts_count > 0) {
          obj["icon"] = `pi pi-folder-plus`;
          obj["style"] = "color: #c9bfd9;";
        }
        if (e.id === parseInt(this.currentCategory.id)) {
          obj["icon"] = `pi pi-folder-open`;
          obj["style"] = "color: #a580e1;";
        }
        return obj;
      };
      let uncategorized = {
        key: 0,
        icon: "pi pi-folder",
        label: `Uncategorized parts (${this.parts_uncategorized_count})`,
        style: 0 === parseInt(this.currentCategory.id) ? "color: #a580e1;" : "",
        parts_count: this.parts_uncategorized_count,
      };

      return [uncategorized, ...[this.categories].map(cb)];
    },
  },
  methods: {
    forceReloadDatas() {
      this.confirm.require({
        message: "Are you sure you want to force reload of all datas ?",
        icon: "pi pi-exclamation-triangle",
        header: "Reload all cached datas",
        rejectProps: {
          label: "No",
          severity: "secondary",
          outlined: true,
        },
        acceptProps: {
          label: "Yes",
          severity: "warn",
        },
        group: "dialog",
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
      navigator.registerProtocolHandler("web+stockazio", `${window.location.origin}/urlhandler?q=%s`, "StockazIO handler");
    },
    doSearch() {
      let search = this.searchTerm.trim();
      this.$refs.searchInput.$el.blur();
      //this.searchTerm = "";

      if (search.startsWith("stockazio://storageLocation/")) {
        // old url handler (location)
        let str = search.split("/");
        let uuid = str[str.length - 1];
        this.$router.replace({ name: "parts-list", query: { storage_uuid: uuid } }).catch(() => {});
      } else if (search.startsWith("web+stockazio:storageLocation,")) {
        // new url handler (location)
        let str = search.split(",");
        let uuid = str[str.length - 1];
        this.$router.replace({ name: "parts-list", query: { storage_uuid: uuid } }).catch(() => {});
      } else if (search.startsWith("stockazio://part/")) {
        // old url handler (part)
        let str = search.split("/");
        let uuid = str[str.length - 1];
        this.$router.replace({ name: "parts-details", params: { partId: uuid } }).catch(() => {});
      } else if (search.startsWith("web+stockazio:part,")) {
        // new url handler (part)
        let str = search.split(",");
        let uuid = str[str.length - 1];
        this.$router.replace({ name: "parts-details", params: { partId: uuid } }).catch(() => {});
      } else if (search.startsWith("{")) {
        // might be a LCSC QrCode
        if (search.endsWith("}")) {
          // then it probably is
          let lcscSplitted = search.replace("{", "").replace("}", "").split(",");
          let pm = lcscSplitted.filter((x) => x.startsWith("pm:"));
          if (pm.length) {
            this.searchTerm = pm[0].replace("pm:", "");
            this.$router.replace({ name: "parts-list", query: { q: pm[0].replace("pm:", "") } }).catch(() => {});
          }
        }
      } else {
        // keyword search
        this.$router.replace({ name: "parts-list", query: { q: search } }).catch(() => {});
      }
    },
    expandAllCategoryChoices() {
      for (let node of this.choicesCategory) {
        this.expandCategoryNode(node);
      }
      this.expandedCategoryKeys = { ...this.expandedCategoryKeys };
    },
    expandCategoryNode(node) {
      if (node.children && node.children.length) {
        this.expandedCategoryKeys[node.key] = true;
        for (let child of node.children) {
          this.expandCategoryNode(child);
        }
      }
    },
    changeCategory(node) {
      console.log(node);
      this.$router.push({
        name: this.categoriesRouteName,
        params: {
          categoryId: node.key,
        },
      });
    },
  },
};
</script>

<style lang="scss" src="./App.scss"></style>
