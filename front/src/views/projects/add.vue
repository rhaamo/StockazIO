<template>
  <div class="add_part">
    <div class="row">
      <div class="col-12">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link :to="{name: 'projects-list'}">
              Projects
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
        <b-form @submit.prevent="addProject">
          <b-row>
            <b-col>
              <b-form-group id="input-group-name" label="Name*" label-for="name">
                <b-form-input
                  id="name"
                  ref="inputname"
                  v-model="form.name"
                  required
                  placeholder="My cool project"
                  :state="$v.form.name.$dirty ? !$v.form.name.$error : null"
                />
                <div v-if="!$v.form.name.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>

              <b-form-group id="input-group-description" label="Description" label-for="description">
                <b-form-input
                  id="description"
                  v-model="form.description"
                  placeholder="Project description"
                  :state="$v.form.description.$dirty ? !$v.form.description.$error : null"
                />
              </b-form-group>

              <b-form-group id="input-group-notes" label="Notes" label-for="notes">
                <b-form-input
                  id="notes"
                  v-model="form.notes"
                  placeholder="Project notes"
                  :state="$v.form.notes.$dirty ? !$v.form.notes.$error : null"
                />
              </b-form-group>

              <b-form-group id="input-group-ibomUrl" label="BOM Url" label-for="ibomUrl">
                <b-form-input
                  id="ibomUrl"
                  v-model="form.ibomUrl"
                  type="url"
                  inputmode="url"
                  :state="$v.form.ibomUrl.$dirty ? !$v.form.ibomUrl.$error : null"
                />
                <div v-if="!$v.form.ibomUrl.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>

              <b-form-group id="input-group-state" label="State:" label-for="state">
                <multiselect v-model="form.state" :options="choicesStates" placeholder="Project state"
                             track-by="value" label="text" required
                             :allow-empty="false"
                />
                <div v-if="!$v.form.state.value.integer || !$v.form.state.value.between || !$v.form.state.value.required || !$v.form.state.required" class="invalid-feedback d-block">
                  Invalid state
                </div>
              </b-form-group>

              <b-form-group id="input-group-state-notes" label="State notes" label-for="state_notes">
                <b-form-input
                  id="state_notes"
                  v-model="form.state_notes"
                  placeholder="blocked by X, waiting for Y"
                  :state="$v.form.state_notes.$dirty ? !$v.form.state_notes.$error : null"
                />
              </b-form-group>

              <b-form-group>
                <b-form-checkbox
                  id="public"
                  v-model="form.public"
                  name="public"
                  :value="true"
                  :unchecked-value="false"
                  inline
                  :state="$v.form.public.$dirty ? !$v.form.public.$error : null"
                >
                  Public
                </b-form-checkbox>
              </b-form-group>

              You will be able to add attachments and parts after saving the project.
              <br>

              <b-button type="submit" variant="primary" class="my-3">
                Add project
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

import { validationMixin } from 'vuelidate'
import { required, maxLength, integer, between } from 'vuelidate/lib/validators'

export default {
  name: 'ProjectsAdd',
  components: {
  },
  mixins: [
    validationMixin
  ],
  data: () => ({
    form: {
      name: '',
      description: '',
      notes: '',
      ibomUrl: '',
      state: { value: 99, text: 'Unknown' },
      state_notes: '',
      public: false
    },
    choicesStates: [
      { value: 1, text: 'Planned' },
      { value: 2, text: 'Ongoing' },
      { value: 3, text: 'Finished' },
      { value: 4, text: 'On-Hold' },
      { value: 5, text: 'Abandonned' },
      { value: 99, text: 'Unknown' }
    ]
  }),
  validations: {
    form: {
      name: {
        required,
        maxLength: maxLength(255)
      },
      description: {
      },
      notes: {},
      ibomUrl: { maxLength: maxLength(255) },
      state: {
        required,
        value: {
          required,
          integer,
          between: between(0, 99)
        }
      },
      state_notes: {
        maxLength: maxLength(255)
      },
      public: {}
    }
  },
  computed: {

  },
  methods: {
    addProject: function () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
        return
      }
      let datas = {
        name: this.form.name,
        description: this.form.description,
        notes: this.form.notes,
        ibom_url: this.form.ibomUrl,
        state: this.form.state.value,
        public: this.form.public,
        state_notes: this.form.state_notes
      }
      apiService.createProject(datas)
        .then((resp) => {
          this.$bvToast.toast(this.$pgettext('Project/Add/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Project/Add/Toast/Success/Title', 'Adding project'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.$router.push({ name: 'projects-details', params: { projectId: resp.data.id } })
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Project/Add/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Project/Add/Toast/Error/Title', 'Adding project'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot save project', error.message)
        })
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
