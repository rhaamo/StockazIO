<template>
  <b-modal
    id="modalStoragesAddCategory" ref="modalStoragesAddCategory"
    size="md" hide-footer @cancel="addCategoryClose"
    @close="addCategoryClose" @hidden="addCategoryClose"
    @show="addCategoryShow"
  >
    <template #modal-header="{ close }">
      <h5 id="modalPartTitle">
        Add storage category
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
                :state="$v.form.name.$dirty ? !$v.form.name.$error : null"
              />
              <div v-if="!$v.form.name.required" class="invalid-feedback d-block">
                Category name is required
              </div>
              <div v-if="!$v.form.name.maxLength" class="invalid-feedback d-block">
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
import { validationMixin } from 'vuelidate'
import { required, maxLength } from 'vuelidate/lib/validators'
import logger from '@/logging'
import { mapState } from 'vuex'
import apiService from '@/services/api/api.service'

export default {
  mixins: [
    validationMixin
  ],
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
    modalAddCategoryParent: null,
    form: {
      name: '',
      parent_id: ''
    }
  }),
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
    addCategoryShow () {
      console.log('parent=', this.parent)
      this.form.parent_id = this.parent
      if (this.item) {
        this.form.name = this.item.name
        this.form.parent_id = this.item.parent
      }
    },
    addCategoryClose () {
      this.clearForm()
      this.$bvModal.hide('modalStoragesAddCategory')
      this.$emit('modal-storages-add-category-closed')
    },
    saveOrUpdate () {
      if (this.mode === 'add') {
        this.save()
      } else {
        this.update()
      }
    },
    save () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('form has errors')
        return
      }

      let storageCategory = {
        name: this.form.name,
        parent: this.form.parent_id
      }

      apiService.createStorageCategory(storageCategory)
      .then(() => {
        this.$bvToast.toast(this.$pgettext('StorageCategory/Add/Toast/Success/Message', 'Success'), {
          title: this.$pgettext('StorageCategory/Add/Toast/Success/Title', 'Add storage category'),
          autoHideDelay: 5000,
          appendToast: true,
          variant: 'primary',
          toaster: 'b-toaster-top-center'
        })
        this.addCategoryClose()
      })
      .catch((error) => {
        this.$bvToast.toast(this.$pgettext('StorageCategory/Add/Toast/Error/Message', 'An error occured, please try again later'), {
          title: this.$pgettext('StorageCategory/Add/Toast/Error/Title', 'Add storage category'),
          autoHideDelay: 5000,
          appendToast: true,
          variant: 'danger',
          toaster: 'b-toaster-top-center'
        })
        logger.default.error('Cannot add storage category', error.message)
      })
    },
    update () {
      console.log('uwu')
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('form has errors')
        return
      }

      let storageCategory = {
        name: this.form.name,
        parent: this.form.parent_id ? this.form.parent_id : null
      }

      apiService.updateStorageCategory(this.item.id, storageCategory)
      .then(() => {
        this.$bvToast.toast(this.$pgettext('StorageCategory/Update/Toast/Success/Message', 'Success'), {
          title: this.$pgettext('StorageCategory/Update/Toast/Success/Title', 'Update storage category'),
          autoHideDelay: 5000,
          appendToast: true,
          variant: 'primary',
          toaster: 'b-toaster-top-center'
        })
        this.addCategoryClose()
      })
      .catch((error) => {
        this.$bvToast.toast(this.$pgettext('StorageCategory/Update/Toast/Error/Message', 'An error occured, please try again later'), {
          title: this.$pgettext('StorageCategory/Update/Toast/Error/Title', 'Update storage category'),
          autoHideDelay: 5000,
          appendToast: true,
          variant: 'danger',
          toaster: 'b-toaster-top-center'
        })
        logger.default.error('Cannot update storage category', error.message)
      })
    },
    clearForm () {
      this.form.name = ''
      this.form.parent_id = ''
      this.$v.$reset()
    }
  }
}
</script>

<style>
</style>
