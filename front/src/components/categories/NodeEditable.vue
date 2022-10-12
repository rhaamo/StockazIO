<template>
  <li class="list-none">
    <i class="fa fa-ellipsis-h mr-2" />
    <span class="text-primary">{{ node.name }}</span>
    <i
      v-tooltip="`Edit`"
      class="fa fa-pencil-square-o ml-2"
      aria-hidden="true"
      @click.prevent="showEditCategory($event, node)"
    ></i>
    <i
      v-tooltip="`Add child category`"
      class="fa fa-plus ml-2 text-green-500"
      aria-hidden="true"
      @click.prevent="showAddCategory($event, node)"
    ></i>
    <i
      v-if="!root"
      v-tooltip="`Delete`"
      class="fa fa-times ml-2 text-red-500"
      aria-hidden="true"
      @click.prevent="deleteItem($event, node)"
    ></i>

    <ul v-if="node.children && node.children.length" class="children">
      <CategoriesNodeEditable
        v-for="child in node.children"
        :key="child.id"
        :node="child"
      />
    </ul>
  </li>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { useUserStore } from "@/stores/user";
import { useOauthStore } from "@/stores/oauth";
import ManageCategoryModal from "@/components/categories/Manage.vue";
import logger from "@/logging";
import { h } from "vue";
import apiService from "@/services/api/api.service";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";

export default {
  name: "CategoriesNodeEditable",
  props: {
    node: Object,
    parent: Object,
    root: {
      type: Boolean,
      default: false,
    },
  },
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    userStore: useUserStore(),
    oauthStore: useOauthStore(),
    confirm: useConfirm(),
    toast: useToast(),
  }),
  computed: {},
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
    showAddCategory($event, parent) {
      this.$dialog.open(ManageCategoryModal, {
        props: {
          modal: true,
          style: {
            width: "15vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add a category")])];
          },
        },
        data: {
          mode: "add",
          parent: parent,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload categories
            this.fetchCategories();
          }
        },
      });
    },
    showEditCategory($event, item) {
      this.$dialog.open(ManageCategoryModal, {
        props: {
          modal: true,
          style: {
            width: "15vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit a category")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
          parent: null,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload categories
            this.fetchCategories();
          }
        },
      });
    },
    deleteItem(event, item) {
      this.confirm.require({
        message: `Are you sure you want to delete the category '${item.name}' ?`,
        header: `Deleting '${item.name}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .deleteCategory(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Category",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchCategories();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Category",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with category deletion", err);
              this.fetchCategories();
            });
        },
        reject: () => {
          return;
        },
      });
    },
  },
};
</script>
