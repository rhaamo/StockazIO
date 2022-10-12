<template>
  <ul class="cat-list">
    <li>
      <i :class="categoryFolderClass(0)" />
      <router-link
        :to="{
          name: categoriesRouteName,
          params: { categoryId: 0 },
        }"
        title="Uncategorized parts"
      >
        Uncategorized parts
        <small>({{ parts_uncategorized_count }})</small>
      </router-link>
    </li>

    <CategoriesNode :node="treeData" />
  </ul>
</template>

<script>
import CategoriesNode from "@/components/categories/node.vue";
import { mapState } from "pinia";
import { useServerStore } from "@/stores/server";
import { useUserStore } from "@/stores/user";
import { useOauthStore } from "@/stores/oauth";
import { usePreloadsStore } from "@/stores/preloads";

export default {
  name: "CategoriesTree",
  components: {
    CategoriesNode,
  },
  props: {
    treeData: Object,
  },
  setup: () => ({
    userStore: useUserStore(),
    oauthStore: useOauthStore(),
    serverStore: useServerStore(),
  }),
  computed: {
    ...mapState(useServerStore, {
      parts_uncategorized_count: (store) =>
        typeof store.parts_uncategorized_count == "number"
          ? store.parts_uncategorized_count
          : "n/a",
    }),
    ...mapState(usePreloadsStore, {
      currentCategory: (store) => store.currentCategory,
    }),
    currentUser() {
      return this.userStore.currentUser && this.oauthStore.loggedIn;
    },
    categoriesRouteName() {
      return this.currentUser
        ? "parts-category-list"
        : "public-parts-category-list";
    },
  },
  methods: {
    categoryFolderClass(category_id) {
      return category_id === parseInt(this.currentCategory.id)
        ? "fa fa-folder-open mr-2"
        : "fa fa-folder-o mr-2";
    },
  },
};
</script>
