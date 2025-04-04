<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div>
      <ul class="list-none">
        <li>
          <router-link v-tooltip.top="'Add storage element on root level'" to="#" class="no-underline" @click.prevent="showAddElementDialog">
            <i class="pi pi-plus" aria-hidden="true" /> Add root storage
          </router-link>

          &nbsp;&nbsp;&nbsp;

          <router-link v-tooltip.top="'Bulk-generate labels'" to="#" class="no-underline" @click.prevent="showBulkLabelGenerator()">
            <i class="pi pi-qrcode" aria-hidden="true" /> Bulk-generate labels
          </router-link>
        </li>
      </ul>
      <template v-for="item in storages">
        <ListItem v-if="item.children" :key="item.id" :item="item" :level="1" />
      </template>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { mapState } from "pinia";
import apiService from "@/services/api/api.service";
import logger from "@/logging";
import { h } from "vue";
import ListItem from "@/components/storages/ListItem.vue";
import ManageItemDialog from "@/components/storages/ManageLocation.vue";
import LabelGeneratorModal from "@/components/label/generator.vue";

export default {
  components: {
    ListItem,
  },
  setup: () => ({
    preloadsStore: usePreloadsStore(),
  }),
  data: () => ({}),
  computed: {
    ...mapState(usePreloadsStore, {
      storages: (store) => {
        return store.storages;
      },
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
            label: "Storages management",
            command: () => {
              this.$router.push({ name: "storages-list" });
            },
          },
        ],
      };
    },
  },
  methods: {
    showBulkLabelGenerator() {
      let slocs = [];
      const cb = (e) => {
        slocs.push(e);
        e.children.forEach(cb);
      };
      this.storages.forEach(cb);

      this.$dialog.open(LabelGeneratorModal, {
        props: {
          modal: true,
          style: {
            width: "70vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("i", { class: "pi pi-qrcode mr-1" }), h("span", "Label Generator")])];
          },
        },
        data: {
          items: slocs,
          kind: "storage",
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
    showAddElementDialog() {
      this.$dialog.open(ManageItemDialog, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add root storage")])];
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
