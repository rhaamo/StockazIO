<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div>
      <ul class="list-none">
        <li>
          <router-link
            to="#"
            title="Add storage category on root level"
            @click.prevent="showAddCategoryDialog"
            class="no-underline"
          >
            <i class="fa fa-plus-square-o" aria-hidden="true" /> Add root
            category
          </router-link>

          &nbsp;&nbsp;&nbsp;

          <router-link
            to="#"
            title="Bulk-generate labels"
            @click.prevent="showBulkLabelGenerator()"
            class="no-underline"
          >
            <i class="fa fa-qrcode" aria-hidden="true" /> Bulk-generate labels
          </router-link>
        </li>
      </ul>
      <template v-for="item in storages">
        <ListCategory
          v-if="item.children && item.storage_locations"
          :key="item.id"
          :item="item"
          :level="1"
        />
        <ListLocation v-else :key="item.uuid" :item="item" />
      </template>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { mapState } from "pinia";
import apiService from "../../services/api/api.service";
import logger from "@/logging";
import { h } from "vue";
import ListCategory from "@/components/storages/ListCategory.vue";
import ListLocation from "@/components/storages/ListLocation.vue";
import ManageCategoryDialog from "@/components/storages/ManageCategory.vue";
import LabelGeneratorModal from "@/components/label/generator.vue";

export default {
  components: {
    ListCategory,
    ListLocation,
  },
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [{ label: "Storages management" }],
    },
  }),
  setup: () => ({
    preloadsStore: usePreloadsStore(),
  }),
  computed: {
    ...mapState(usePreloadsStore, {
      storages: (store) => {
        return store.storages;
      },
    }),
  },
  methods: {
    showBulkLabelGenerator() {
      let slocs = [];
      const cb = (e) => {
        if (e.category) {
          slocs.push(e);
        } else {
          e.storage_locations.forEach(cb);
          e.children.forEach(cb);
        }
      };
      this.storages.forEach(cb);

      this.$dialog.open(LabelGeneratorModal, {
        props: {
          modal: true,
          style: {
            width: "70vw",
          },
        },
        templates: {
          header: () => {
            return [
              h("h3", [
                h("i", { class: "fa fa-qrcode mr-1" }),
                h("span", "Label Generator"),
              ]),
            ];
          },
        },
        data: {
          items: slocs,
        },
      });
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
    showAddCategoryDialog() {
      this.$dialog.open(ManageCategoryDialog, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add root category")])];
          },
        },
        data: {
          name: "",
          parent_id: null,
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
