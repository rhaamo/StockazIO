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
        <b-form @submit.prevent="updateProject">
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
              </b-form-group>

              <b-form-group id="input-group-state" label="State:" label-for="state">
                <multiselect v-model="form.state" :options="choicesStates" placeholder="Project state"
                             track-by="value" label="text" required
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

              <b-button type="submit" variant="primary" class="my-3">
                Save project
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
import { required } from 'vuelidate/lib/validators'

export default {
  components: {
  },
  mixins: [
    validationMixin
  ],
  data: () => ({
    project: null,
    form: {
      name: '',
      description: '',
      notes: '',
      ibomUrl: '',
      state: { value: 99, text: 'Unknown' },
      public: false
    },
    choicesStates: [
      { value: 1, text: 'Planned' },
      { value: 2, text: 'Ongoing' },
      { value: 3, text: 'Finished' },
      { value: 4, text: 'Waiting' },
      { value: 5, text: 'Abandonned' },
      { value: 99, text: 'Unknown' }
    ]
  }),
  validations: {
    form: {
      name: {
        required
      },
      description: {
      },
      notes: {},
      ibomUrl: {},
      state: {
        required
      },
      public: {}
    }
  },
  computed: {
    projectId () {
      return this.$route.params.projectId
    }
  },
  created () {
    this.fetchProject()
  },
  methods: {
    fetchProject () {
      apiService.getProject(this.projectId)
        .then((res) => {
          this.project = res.data
          this.form.name = this.project.name
          this.form.description = this.project.description
          this.form.notes = this.project.notes
          this.form.ibomUrl = this.project.ibom_url
          let state = this.choicesStates.filter(function (e) { return e.value === res.data.state })
          this.form.state = state
          this.form.public = this.project.public
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('Project/Details/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Project/Details/Toast/Error/Title', 'Fetching project details'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error with fetching project', err.message)
        })
    },
    updateProject: function () {
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
        public: this.form.public
      }
      apiService.updateProject(this.project.id, datas)
        .then(() => {
          this.$bvToast.toast(this.$pgettext('Project/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Project/Update/Toast/Success/Title', 'Updating project'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.$router.push({ name: 'projects-details', params: { projectId: this.project.id } })
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Project/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Project/Update/Toast/Error/Title', 'Updating project'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot update project', error.message)
        })
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
