<template>
  <div>
    <li class="list-none mt-1">
      <i class="fa fa-folder-o" aria-hidden="true" /> {{ item.name }}

      <template v-if="item.picture">
        &nbsp;
        <i
          :id="item.uuid"
          class="fa fa-file-image-o"
          aria-hidden="true"
          v-tooltip="`Click to show picture`"
          @click.prevent="$refs.storage_picture.toggle($event)"
        />
        <OverlayPanel
          ref="storage_picture"
          appendTo="body"
          :showCloseIcon="true"
          id="storage_picture"
        >
          <Image preview width="250" :src="item.picture_medium"></Image>
        </OverlayPanel>
      </template>

      &nbsp;&nbsp;

      <router-link
        to="#"
        v-tooltip="`QrCode label generator`"
        @click.prevent="showLabelGeneratorModal(item)"
        class="no-underline"
      >
        <i class="fa fa-qrcode" aria-hidden="true" />
      </router-link>

      <template v-if="!readonly">
        &nbsp;&nbsp;

        <router-link
          to="#"
          v-tooltip="`Edit Location`"
          @click.prevent="showEditLocationModal(item)"
          class="no-underline"
        >
          <i class="fa fa-pencil-square-o" aria-hidden="true" />
        </router-link>
        &nbsp;
        <router-link
          to="#"
          v-tooltip="`Delete Location`"
          @click.prevent="showDeleteLocationModal(item)"
          class="no-underline"
        >
          <i class="fa fa-trash-o" aria-hidden="true" />
        </router-link>
      </template>
      <br />
      <template v-if="item.description">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&raquo; {{ item.description }}
      </template>
    </li>
  </div>
</template>

<script>
import ManageLocationDialog from "@/components/storages/ManageLocation.vue";
import { h } from "vue";
import apiService from "../../services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";
import { usePreloadsStore } from "@/stores/preloads";
import LabelGeneratorModal from "@/components/label/generator.vue";

export default {
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
    confirm: useConfirm(),
    preloadsStore: usePreloadsStore(),
  }),
  methods: {
    showLabelGeneratorModal(item) {
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
          items: [this.item],
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
    showEditLocationModal(item) {
      this.$dialog.open(ManageLocationDialog, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit storage location")])];
          },
        },
        data: {
          id: item.id,
          name: item.name,
          parent_id: { [item.category]: true },
          description: item.description,
          picture: item.picture,
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
    showDeleteLocationModal(item) {
      this.confirm.require({
        message: `Are you sure you want to delete the location '${item.name}' ?`,
        header: `Deleting '${item.name}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .deleteStorageLocation(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Storage location",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchStorages();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Storage location",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with storage location deletion", err);
              this.fetchStorages();
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
