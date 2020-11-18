<template>
  <b-modal id="modalAddExternalPart" ref="modalAddExternalPart"
           size="lg" hide-footer @cancel="partModalClose"
           @close="partModalClose" @hidden="partModalClose"
  >
    <template #modal-header="{ close }">
      <h5 id="modalPartTitle">
        Describe part
      </h5>
      <button type="button" class="close" data-dismiss="modal"
              aria-label="Close" @click="close()"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </template>

    <div class="container">
      <div class="row">
        <div class="col-md-11 mx-auto">
          <b-form @submit.prevent="save">
            <b-form-group id="input-group-name" label="Name*" label-for="name">
              <b-form-input
                id="name"
                ref="inputname"
                v-model="form.part_name"
                required
                placeholder="PIC42ACHU"
                :state="$v.form.part_name.$dirty ? !$v.form.part_name.$error : null"
              />
            </b-form-group>

            <b-form-group id="input-group-qty" label="Qty*" label-for="qty">
              <b-form-input
                id="qty"
                v-model="form.qty"
                required
                type="number"
                inputmode="numeric"
                :state="$v.form.qty.$dirty ? !$v.form.qty.$error : null"
              />
            </b-form-group>

            <b-form-group id="input-group-notes" label="Notes" label-for="notes">
              <b-form-input
                id="notes"
                ref="inputnotes"
                v-model="form.notes"
                :state="$v.form.notes.$dirty ? !$v.form.notes.$error : null"
              />
            </b-form-group>

            <b-form-group>
              <b-form-checkbox
                id="sourced"
                v-model="form.sourced"
                name="sourced"
                :value="true"
                :unchecked-value="false"
                inline
                :state="$v.form.sourced.$dirty ? !$v.form.sourced.$error : null"
              >
                Sourced
              </b-form-checkbox>
            </b-form-group>

            <b-button type="submit" variant="primary">
              Add part
            </b-button>
          </b-form>
        </div>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, minValue } from 'vuelidate/lib/validators'

export default {
  mixins: [
    validationMixin
  ],
  props: {
  },
  data: () => ({
    form: {
      part_name: '',
      qty: 1,
      sourced: false,
      notes: ''
    }
  }),
  validations: {
    form: {
      part_name: { required },
      qty: {
        required,
        minValue: minValue(0)
      },
      sourced: {},
      notes: {}
    }
  },
  computed: {
  },
  methods: {
    partModalClose () {
      this.$bvModal.hide('modalAddExternalPart')
      this.$emit('add-part-external-modal-closed')
    },
    save () {
      // todo check form + api call
      this.$bvModal.hide('modalAddExternalPart')
      this.$emit('add-part-external-saved')
    }
  }
}
</script>
