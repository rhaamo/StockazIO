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
export default {
  props: {
    item: Object,
    level: Number,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    showLabelGeneratorModal(item) {
      console.log("showLabelGeneratorModal", item);
    },
    showEditLocationModal(item) {
      console.log("showEditLocationModal", item);
    },
    showDeleteLocationModal(item) {
      console.log("showDeleteLocationModal", item);
    },
  },
};
</script>
