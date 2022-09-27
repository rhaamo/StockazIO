<template>
  <li>
    <template v-if="node.parts_count > 0">
      <i :class="categoryFolderClass(node)" />
      <router-link
        :to="{
          name: categoriesRouteName,
          params: {
            categoryId: node.id,
          },
        }"
        :title="node.name"
      >
        <b
          >{{ node.name }} <small>({{ node.parts_count }})</small></b
        >
      </router-link>
    </template>
    <template v-else>
      <i :class="categoryFolderClass(node)" />
      <router-link
        :to="{
          name: categoriesRouteName,
          params: {
            categoryId: node.id,
          },
        }"
        :title="node.name"
      >
        {{ node.name }} <small>({{ node.parts_count }})</small>
      </router-link>
    </template>

    <ul v-if="node.children && node.children.length" class="children">
      <CategoriesNode
        v-for="child in node.children"
        :key="child.id"
        :node="child"
      />
    </ul>
  </li>
</template>

<script>
import { mapState } from "pinia";
import { usePreloadsStore } from "@/stores/preloads";
import { useUserStore } from "@/stores/user";
import { useOauthStore } from "@/stores/oauth";

export default {
  name: "CategoriesNode",
  props: {
    node: Object,
  },
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    userStore: useUserStore(),
    oauthStore: useOauthStore(),
  }),
  computed: {
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
    categoryFolderClass(category) {
      return category.id === this.currentCategory.id
        ? "fa fa-folder-open-o mr-2"
        : "fa fa-folder mr-2";
    },
  },
};
</script>
