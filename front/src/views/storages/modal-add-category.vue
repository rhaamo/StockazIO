<template>
  <b-modal
    id="modalStoragesAddCategory" ref="modalStoragesAddCategory"
    size="xl" hide-footer @cancel="partModalClose"
    @close="partModalClose" @hidden="partModalClose"
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
          <b-form @submit.prevent="save">

            parent: {{ parent || 'root' }}<br/>

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
import logger from '@/logging'

export default {
  mixins: [
    validationMixin
  ],
  props: {
    parent: {
      type: Number
    }
  },
  data: () => ({
    modalAddCategoryParent: null,
    form: {
    }
  }),
  validations: {
    form: {
    }
  },
  computed: {
  },
  methods: {
    partModalClose () {
      this.clearForm()
      this.$bvModal.hide('modalStoragesAddCategory')
      this.$emit('modal-storages-add-category-closed')
    },
    save () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('form has errors')
        // return
      }
    },
    clearForm () {
      this.$v.$reset()
    }
  }
}
</script>

<style>
</style>
