<template>
  <li>
    <i class="fa fa-folder-o" aria-hidden="true" /> {{ item.name }}

    <template v-if="item.picture">
        &nbsp;
      <i
        :id="item.uuid"
        class="fa fa-file-image-o"
        aria-hidden="true"
      />
      <b-popover
        :target="item.uuid"
        placement="right"
        triggers="hover focus"
      >
        <template #title>
          Storage Picture
        </template>
        <img :src="item.picture_medium" width="250px">
      </b-popover>
    </template>

    &nbsp;&nbsp;

    <router-link to="#" title="Edit Location" @click.native.prevent="editLocation(item)">
      <i
        class="fa fa-pencil-square-o"
        aria-hidden="true"
      />
    </router-link>
            &nbsp;
    <router-link to="#" title="Delete Location" @click.native.prevent="deleteLocation(item)">
      <i
        class="fa fa-trash-o"
        aria-hidden="true"
      />
    </router-link>
    <br>
    <template v-if="item.description">
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&raquo; {{ item.description }}
    </template>
  </li>
</template>

<script>
import logger from '@/logging'
import apiService from '@/services/api/api.service'

export default {
  name: 'ListLocation',
  props: {
    'item': Object,
    'level': Number
  },
  computed: {
  },
  methods: {
    editLocation (item) {
      this.$root.$emit('changeModalManageLocationMode', 'edit')
      this.$root.$emit('modalStoragesLocationUpdateSetItem', item)
      // Important to nextTick otherwise we don't get the time to emit the parent ID change
      this.$nextTick(() => {
        this.$bvModal.show('modalStoragesManageLocation')
      })
    },
    deleteLocation (item) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the location '${item.name}' ?`, {
        title: 'Please Confirm',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: 'YES',
        cancelTitle: 'NO',
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true
      })
        .then((value) => {
          if (value === false) { return }

          if (value === true) {
            apiService.deleteStorageLocation(item.id)
              .then((val) => {
                this.$bvToast.toast(this.$pgettext('StorageLocation/Delete/Toast/Success/Message', 'Success'), {
                  title: this.$pgettext('StorageLocation/Delete/Toast/Success/Title', 'Deleting location'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'primary',
                  toaster: 'b-toaster-top-center'
                })
                // triggers a reload of the storage tree
                this.$nextTick(() => {
                  this.$root.$emit('reloadStorageCategoriesTree')
                })
              })
              .catch((err) => {
                this.$bvToast.toast(this.$pgettext('StorageLocation/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                  title: this.$pgettext('StorageLocation/Delete/Toast/Error/Title', 'Deleting location'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'danger',
                  toaster: 'b-toaster-top-center'
                })
                logger.default.error('Error with storage location deletion', err)
                // triggers a reload of the storage tree
                this.$root.$emit('reloadStorageCategoriesTree')
              })
          }
        })
    }
  }
}
</script>
