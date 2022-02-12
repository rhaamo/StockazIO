<template>
  <ul class="list_storages">
    <li>
        <i class="fa fa-home" aria-hidden="true"></i> {{ item.name }}

        &nbsp;&nbsp;

        <router-link to="#" @click.native.prevent="editCategory(item)" title="Edit Category">
            <i
            class="fa fa-pencil-square-o"
            aria-hidden="true"
            />
        </router-link>
            &nbsp;
        <router-link to="#" @click.native.prevent="deleteCategory(item)" title="Delete Category">
            <i
            class="fa fa-trash-o"
            aria-hidden="true"
            />
        </router-link>

        &nbsp;&nbsp;

        <b-button pill size="sm" variant="light"
        to="#"
        @click.native.prevent="addCategory(item.id)"
        :title="addCategoryTitle(item.name)">
          <i class="fa fa-home" aria-hidden="true"></i>&nbsp;
          <i class="fa fa-plus" aria-hidden="true"></i>
        </b-button>

        &nbsp;&nbsp;
        <b-button pill size="sm" variant="info"
        to="#"
        @click.native.prevent="addLocation(item.id)"
        :title="addLocationTitle(item.name)">
          <i class="fa fa-folder-o" aria-hidden="true"></i>&nbsp;
          <i class="fa fa-plus" aria-hidden="true"></i>
        </b-button>
    </li>
    <ListCategory v-for="item in item.children" :key="item.id"
    :item=item
    :level="level+1"></ListCategory>
    <ul class="list_storages"><ListLocation v-for="item in item.storage_locations" :key="item.uuid" :item=item
    :level="level+1"></ListLocation></ul>
  </ul>
</template>

<script>
import ListLocation from './list-location'
import logger from '@/logging'
import apiService from '@/services/api/api.service'

export default {
  name: 'ListCategory',
  components: {
    ListLocation
  },
  props: {
    'item': Object,
    'level': Number
  },
  computed: {
      
  },
  methods: {
    addCategory (id) {
        this.$root.$emit('changeModalManageCategoryParent', id)
        this.$root.$emit('changeModalManageCategoryMode', 'add')
        // Important to nextTick otherwise we don't get the time to emit the parent ID change
        this.$nextTick(() => {
            this.$bvModal.show('modalStoragesManageCategory')
        })
    },
    addCategoryTitle (name) {
        return `Add category under '${name}'`
    },
    addLocationTitle (name) {
        return `Add location/box under '${name}'`
    },
    editCategory (item) {
        this.$root.$emit('changeModalManageCategoryMode', 'edit')
        this.$root.$emit('modalStoragesCategoryUpdateSetItem', item)
        // Important to nextTick otherwise we don't get the time to emit the parent ID change
        this.$nextTick(() => {
            this.$bvModal.show('modalStoragesManageCategory')
        })
    },
    deleteCategory (item) {
        this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the category '${item.name}' ?`, {
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
                apiService.deleteStorageCategory(item.id)
                .then((val) => {
                    this.$bvToast.toast(this.$pgettext('StorageCategory/Delete/Toast/Success/Message', 'Success'), {
                        title: this.$pgettext('StorageCategory/Delete/Toast/Success/Title', 'Deleting category'),
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
                    this.$bvToast.toast(this.$pgettext('StorageCategory/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                    title: this.$pgettext('StorageCategory/Delete/Toast/Error/Title', 'Deleting category'),
                    autoHideDelay: 5000,
                    appendToast: true,
                    variant: 'danger',
                    toaster: 'b-toaster-top-center'
                    })
                    logger.default.error('Error with storage category deletion', err)
                    // triggers a reload of the storage tree
                    this.$root.$emit('reloadStorageCategoriesTree')
                })
            }
        })
    }
  }
}
</script>
