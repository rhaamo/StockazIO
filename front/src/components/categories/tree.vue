<template>
  <ul class="cat-list">
    <li>
      <i class="fa fa-folder-o mr-1" />
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
import CategoriesNode from "./node.vue";
import { mapState } from "pinia";
import { useServerStore } from "@/stores/server";
import { useUserStore } from "@/stores/user";
import { useOauthStore } from "@/stores/oauth";

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
    currentUser() {
      return this.userStore.currentUser && this.oauthStore.loggedIn;
    },
    categoriesRouteName() {
      return this.currentUser
        ? "parts-category-list"
        : "public-parts-category-list";
    },
  },
};
</script>
