<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div>
      <ul class="list-none">
        <li>
          <router-link
            to="#"
            v-tooltip="'Add storage element on root level'"
            @click.prevent="showAddElementDialog"
            class="no-underline"
          >
            <i class="fa fa-plus-square-o" aria-hidden="true" /> Add root
            storage
          </router-link>

          &nbsp;&nbsp;&nbsp;

          <router-link
            to="#"
            v-tooltip="'Bulk-generate labels'"
            @click.prevent="showBulkLabelGenerator()"
            class="no-underline"
          >
            <i class="fa fa-qrcode" aria-hidden="true" /> Bulk-generate labels
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
  data: () => ({
    breadcrumb: {
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
