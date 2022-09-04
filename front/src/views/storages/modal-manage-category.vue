<template>
  <b-modal
    id="modalStoragesManageCategory" ref="modalStoragesManageCategory"
    size="md" hide-footer @cancel="manageCategoryClose"
    @close="manageCategoryClose" @hidden="manageCategoryClose"
    @show="manageCategoryShow"
  >
    <template #modal-header="{ close }">
      <h5 id="modalPartTitle">
        Manage storage category
      </h5>
      <button
        type="button" class="close" data-dismiss="modal"
        aria-label="Close" @click="close()"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </template>

    <div class="container">
      <div class="row">
        <div class="col-md-11 mx-auto">
          <b-form @submit.prevent="saveOrUpdate">
            <b-form-group id="input-group-name" label="Name" label-for="name">
              <b-form-input
                id="name"
                ref="inputname"
                v-model="form.name"
                required
                placeholder="Under the bed"
                :state="v$.form.name.$dirty ? !v$.form.name.$error : null"
                autofocus
              />
              <div v-if="!v$.form.name.required" class="invalid-feedback d-block">
                Category name is required
              </div>
              <div v-if="!v$.form.name.maxLength" class="invalid-feedback d-block">
                Maximum length is 200
              </div>
            </b-form-group>

            <b-form-group id="input-group-storage_location" label="Parent storage category:" label-for="storage_location">
              <vue-treeselect
                v-model="form.parent_id" :multiple="false" :options="choicesStorageLocation"
                search-nested :default-expand-level="Infinity" clearable
                no-children-text placeholder="In the House ? The Workshop ?"
                :disable-branch-nodes="false"
              />
            </b-form-group>

            <b-button class="mt-3" type="submit" variant="primary">
              Save
            </b-button>
          </b-form>
        </div>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { required, maxLength } from '@vuelidate/validators'
import logger from '@/logging'
import { mapState } from 'vuex'
import apiService from '@/services/api/api.service'
import { useToast } from 'vue-toastification'
import ToastyToast from '@/components/toasty-toast'
import useVuelidate from '@vuelidate/core'

export default {
  props: {
    parent: {
      type: Number
    },
    mode: {
      type: String
    },
    item: {
      type: Object
    }
  },
  data: () => ({
    modalManageCategoryParent: null,
    form: {
      name: '',
      parent_id: ''
    }
  }),
  setup () {
    const toast = useToast()
    const v$ = useVuelidate()
    return { toast, v$ }
  },
  validations: {
    form: {
      name: { required, maxLength: maxLength(200) },
      parent_id: {}
    }
  },
  computed: {
    ...mapState({
      choicesStorageLocation: (state) => {
        const cb = (e) => {
          return {
            id: e.id,
            label: e.name,
            children: e.children && e.children.length ? e.children.map(cb) : 0
          }
        }
        return state.preloads.storages.map(cb)
      }
    })
  },
  methods: {
    manageCategoryShow () {
      this.form.parent_id = this.parent
      if (this.item) {
        this.form.name = this.item.name
        this.form.parent_id = this.item.parent
      }
    },
    manageCategoryClose () {
      this.clearForm()
      this.$bvModal.hide('modalStoragesManageCategory')
      this.$emit('modal-storages-manage-category-closed')
    },
    saveOrUpdate () {
      if (this.mode === 'add') {
        this.save()
      } else {
        this.update()
      }
    },
    save () {
      this.v$.$touch()
      if (this.v$.$invalid) {
        logger.default.error('form has errors')
        return
      }

      let storageCategory = {
        name: this.form.name,
        parent: this.form.parent_id
      }

      apiService.createStorageCategory(storageCategory)
        .then(() => {
          this.toast.success({
            component: ToastyToast,
            props: {
              title: this.$pgettext('StorageCategory/Add/Toast/Success/Title', 'Add storage category'),
              message: this.$pgettext('StorageCategory/Add/Toast/Success/Message', 'Success')
            }
          })
          this.manageCategoryClose()
        })
        .catch((error) => {
          this.toast.error({
            component: ToastyToast,
            props: {
              title: this.$pgettext('StorageCategory/Add/Toast/Error/Title', 'Add storage category'),
              message: this.$pgettext('StorageCategory/Add/Toast/Error/Message', 'An error occured, please try again later')
            }
          })
          logger.default.error('Cannot add storage category', error.message)
        })
    },
    update () {
      this.v$.$touch()
      if (this.v$.$invalid) {
        logger.default.error('form has errors')
        return
      }

      let storageCategory = {
        name: this.form.name,
        parent: this.form.parent_id ? this.form.parent_id : null
      }

      apiService.updateStorageCategory(this.item.id, storageCategory)
        .then(() => {
          this.toast.success({
            component: ToastyToast,
            props: {
              title: this.$pgettext('StorageCategory/Update/Toast/Success/Title', 'Update storage category'),
              message: this.$pgettext('StorageCategory/Update/Toast/Success/Message', 'Success')
            }
          })
          this.manageCategoryClose()
        })
        .catch((error) => {
          this.toast.error({
            component: ToastyToast,
            props: {
              title: this.$pgettext('StorageCategory/Update/Toast/Error/Title', 'Update storage category'),
              message: this.$pgettext('StorageCategory/Update/Toast/Error/Message', 'An error occured, please try again later')
            }
          })
          logger.default.error('Cannot update storage category', error.message)
        })
    },
    clearForm () {
      this.form.name = ''
      this.form.parent_id = ''
      this.v$.$reset()
    }
  }
}
</script>

<style>
</style>
