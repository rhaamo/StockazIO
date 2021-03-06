<template>
  <div class="add_part_parameters_preset">
    <div class="row">
      <div class="col-12">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link :to="{ name: 'parameters-presets-list' }">
              Part Parameters Presets
            </router-link>
          </li>
          <li class="breadcrumb-item active">
            Add new one
          </li>
        </ol>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-md-6 mx-auto">
        <b-form @submit.prevent="addPreset">
          <b-row>
            <b-col>
              <b-form-group id="input-group-name" label="Name*" label-for="name">
                <b-form-input
                  id="name"
                  ref="inputname"
                  v-model="form.name"
                  required
                  placeholder="Capacitor XXX"
                  :state="$v.form.name.$dirty ? !$v.form.name.$error : null"
                />
                <div v-if="!$v.form.name.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>

              <hr>

              <div v-for="(_, i) in form.part_parameters_presets" :key="i">
                <b-row>
                  <b-col>
                    <b-form-group :id="itemId('name', i)" label="Name*" :label-for="itemId('name', i)">
                      <b-form-input
                        :id="itemId('name', i)"
                        v-model="form.part_parameters_presets[i].name"
                        required
                      />
                      <div v-if="!$v.form.part_parameters_presets.$each[i].name.required" class="invalid-feedback d-block">
                        Name is required
                      </div>
                      <div v-if="!$v.form.part_parameters_presets.$each[i].name.maxLength" class="invalid-feedback d-block">
                        Maximum length is 255
                      </div>
                    </b-form-group>
                  </b-col>
                  <b-col>
                    <b-form-group :id="itemId('description', i)" label="Description" :label-for="itemId('description', i)">
                      <b-form-input
                        :id="itemId('description', i)"
                        v-model="form.part_parameters_presets[i].description"
                      />
                      <div v-if="!$v.form.part_parameters_presets.$each[i].description.maxLength" class="invalid-feedback d-block">
                        Maximum length is 255
                      </div>
                    </b-form-group>
                  </b-col>
                </b-row>
                <b-row>
                  <b-col>
                    <b-form-group :id="itemId('unit', i)" label="Unit:" :label-for="itemId('unit', i)">
                      <multiselect v-model="form.part_parameters_presets[i].unit"
                                   :options="choicesPartParametersUnit"
                                   label="text" track-by="value"
                      />
                    </b-form-group>
                  </b-col>
                </b-row>
                <BtnDeleteInline size="sm" btn-variant-main="danger" btn-variant-ok="success"
                                 btn-variant-cancel="danger" btn-main-text="remove item"
                                 btn-main-text-disabled="Confirm ?" btn-ok-text="Yes"
                                 btn-cancel-text="No" @action-confirmed="deleteItem(i)"
                />
                <hr>
              </div>

              <div>
                <b-button size="sm" variant="info" @click.prevent="addItem">
                  add item
                </b-button>
              </div>

              <b-button type="submit" variant="primary" class="my-3">
                Add preset
              </b-button>
            </b-col>
          </b-row>
        </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import logger from '@/logging'
import apiService from '@/services/api/api.service'
import BtnDeleteInline from '@/components/btn_delete_inline'

import { validationMixin } from 'vuelidate'
import { required, maxLength } from 'vuelidate/lib/validators'
import { mapState } from 'vuex'

export default {
  components: {
    BtnDeleteInline
  },
  mixins: [
    validationMixin
  ],
  data: () => ({
    form: {
      name: '',
      part_parameters_presets: []
    }
  }),
  validations: {
    form: {
      name: {
        required,
        maxLength: maxLength(255)
      },
      part_parameters_presets: {
        $each: {
          name: { required, maxLength: maxLength(255) },
          description: { maxLength: maxLength(255) },
          unit: {}
        }
      }
    }
  },
  computed: {
    ...mapState({
      choicesPartParametersUnit: (state) => {
        return state.preloads.parameters_unit.map(x => { return { value: x.id, text: `${x.name} (${x.symbol})` } })
      }
    })
  },
  methods: {
    addPreset: function () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
        return
      }
      let datas = {
        name: this.form.name,
        part_parameters_presets: this.form.part_parameters_presets.map(x => {
          if (x.name !== '') {
            return { name: x.name, description: x.description, unit: x.unit ? x.unit.value : null }
          }
        })
      }
      apiService.createPartParameterPresets(datas)
        .then((resp) => {
          this.$bvToast.toast(this.$pgettext('Preset/Add/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Preset/Add/Toast/Success/Title', 'Adding preset'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.$store.dispatch('preloadPartParametersPresets')
          this.$router.push({ name: 'parameters-presets-details', params: { presetId: resp.data.id } })
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Preset/Add/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Preset/Add/Toast/Error/Title', 'Adding preset'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot save preset', error.message)
        })
    },
    itemId (func, idx) {
      return `input-item-${func}-${idx}`
    },
    addItem () {
      this.form.part_parameters_presets.push({
        name: '',
        description: '',
        unit: null
      })
    },
    deleteItem (idx) {
      this.$delete(this.form.part_parameters_presets, idx)
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
