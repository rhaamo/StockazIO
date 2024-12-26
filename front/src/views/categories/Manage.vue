<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-4 ml-4 list-none">
      <ul class="cat-list">
        <CategoriesNodeEditable :node="categories" :root="true" />
      </ul>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { mapState } from "pinia";
import apiService from "@/services/api/api.service";
import logger from "@/logging";
import CategoriesNodeEditable from "@/components/categories/NodeEditable.vue";

export default {
  components: {
    CategoriesNodeEditable,
  },
  setup: () => ({
    preloadsStore: usePreloadsStore(),
  }),
  data: () => ({}),
  computed: {
    ...mapState(usePreloadsStore, {
      categories: (store) => store.categories,
    }),
    breadcrumb() {
      return {
        home: {
          icon: "pi pi-home",
          command: () => {
            this.$router.push({ name: "home" });
          },
        },
        items: [
          {
            label: "Categories",
            command: () => {
              this.$router.push({ name: "categories-list" });
            },
          },
        ],
      };
    },
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    fetchCategories() {
      logger.default.info("reloading categories");
      apiService
        .getCategories()
        .then((val) => {
          this.preloadsStore.setCategories(val.data[0]);
          this.preloadsStore.setLastUpdate("categories", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Categories",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching categories", err);
        });
    },
  },
};
</script>
