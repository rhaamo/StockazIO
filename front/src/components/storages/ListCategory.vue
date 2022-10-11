<template>
  <div>
    <ul class="list-none mt-1">
      <li class="mt-1 list-none">
        <i class="fa fa-home" aria-hidden="true" /> {{ item.name }}

        <template v-if="!readonly">
          &nbsp;&nbsp;

          <router-link
            to="#"
            v-tooltip="`Edit Category`"
            @click.prevent="editCategoryModal(item)"
            class="no-underline"
          >
            <i class="fa fa-pencil-square-o" aria-hidden="true" />
          </router-link>
          &nbsp;
          <router-link
            to="#"
            v-tooltip="`Delete Category`"
            @click.prevent="deleteCategoryModal(item)"
            class="no-underline"
          >
            <i class="fa fa-trash-o" aria-hidden="true" />
          </router-link>

          &nbsp;&nbsp;

          <router-link
            to="#"
            v-tooltip="`${addCategoryTitle(item.name)}`"
            @click.prevent="addCategoryModal(item.id)"
            class="no-underline"
          >
            [add category]
          </router-link>

          &nbsp;&nbsp;
          <router-link
            to="#"
            v-tooltip="`${addLocationTitle(item.name)}`"
            @click.prevent="addLocationModal(item.id)"
            class="no-underline"
          >
            [add location/box]
          </router-link>
        </template>
      </li>
      <ListCategory
        v-for="category in item.children"
        :key="category.id"
        :item="category"
        :level="level + 1"
        :readonly="readonly"
      />
      <ul class="mt-1">
        <ListLocation
          v-for="storage in item.storage_locations"
          :key="storage.uuid"
          :item="storage"
          :level="level + 1"
          :readonly="readonly"
        />
      </ul>
    </ul>
  </div>
</template>

<script>
import ListLocation from "@/components/storages/ListLocation.vue";
import { h } from "vue";
import ManageCategoryDialog from "@/components/storages/ManageCategory.vue";
import ManageLocationDialog from "@/components/storages/ManageLocation.vue";
import apiService from "@/services/api/api.service";
import logger from "@/logging";
import { useToast } from "primevue/usetoast";
import { usePreloadsStore } from "@/stores/preloads";
import { useConfirm } from "primevue/useconfirm";

export default {
  components: {
    ListLocation,
  },
  props: {
    item: Object,
    level: Number,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  setup: () => ({
    toast: useToast(),
    preloadsStore: usePreloadsStore(),
    confirm: useConfirm(),
  }),
  methods: {
    addCategoryTitle(name) {
      return `Add category under '${name}'`;
    },
    addLocationTitle(name) {
      return `Add location/box under '${name}'`;
    },
    fetchStorages() {
      logger.default.info("reloading storages");
      apiService
        .getStorages()
        .then((val) => {
          this.preloadsStore.setStorages(val.data);
          this.preloadsStore.setLastUpdate("storages", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Storages",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching storages", err);
        });
    },
    editCategoryModal(item) {
      this.$dialog.open(ManageCategoryDialog, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit category")])];
          },
        },
        data: {
          id: item.id,
          name: item.name,
          parent_id: { [item.parent]: true },
          mode: "edit",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload storages
            this.fetchStorages();
          }
        },
      });
    },
    deleteCategoryModal(item) {
      this.confirm.require({
        message: `Are you sure you want to delete the category '${item.name}' ?`,
        header: `Deleting '${item.name}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .deleteStorageCategory(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Storage category",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchStorages();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Storage category",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with storage category deletion", err);
              this.fetchStorages();
            });
        },
        reject: () => {
          return;
        },
      });
    },
    addCategoryModal(id) {
      this.$dialog.open(ManageCategoryDialog, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add category")])];
          },
        },
        data: {
          name: "",
          parent_id: { [id]: true },
          mode: "add",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload storages
            this.fetchStorages();
          }
        },
      });
    },
    addLocationModal(id) {
      this.$dialog.open(ManageLocationDialog, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add storage location")])];
          },
        },
        data: {
          name: "",
          parent_id: { [id]: true },
          description: "",
          picture: "",
          mode: "add",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload storages
            this.fetchStorages();
          }
        },
      });
    },
  },
};
</script>
