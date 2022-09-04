<template>
  <div class="label_templates_list">
    <div class="row">
      <div class="col-8">
        <ol class="breadcrumb">
          <li class="breadcrumb-item active">
            <router-link :to="{ name: 'label-templates-list' }">
              Label Templates
            </router-link>
          </li>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-2">
        <b-list-group>
          <b-list-group-item :active="labelTemplate == null" @click.prevent="switchToTab(null)">
            Add new
          </b-list-group-item>
          <b-list-group-item
            v-for="item in labelTemplates" :key="item.id" :active="labelTemplate && labelTemplate.id == item.id"
            @click.prevent="switchToTab(item)"
          >
            {{ item.name }}
          </b-list-group-item>
        </b-list-group>
      </div>

      <div class="col-4">
        <b-form @submit.prevent="save">
          <b-form-group id="input-group-name" label="Name" label-for="name">
            <b-form-input
              id="name"
              ref="inputname"
              v-model="form.name"
              required
              placeholder="Brother 69x42mm"
              :state="v$.form.name.$dirty ? !v$.form.name.$error : null"
            />
            <div v-if="!v$.form.name.required" class="invalid-feedback d-block">
              Template name is required
            </div>
            <div v-if="!v$.form.name.maxLength" class="invalid-feedback d-block">
              Maximum length is 255
            </div>
          </b-form-group>

          <b-form-group id="input-group-width" label="Width" label-for="width">
            <b-form-input
              id="width"
              ref="inputwidth"
              v-model="form.width"
              required
              placeholder="69"
              :state="v$.form.width.$dirty ? !v$.form.width.$error : null"
              type="number"
              description="In mm"
            />
            <div v-if="!v$.form.width.required" class="invalid-feedback d-block">
              Width is required
            </div>
          </b-form-group>

          <b-form-group id="input-group-height" label="Height" label-for="height">
            <b-form-input
              id="height"
              ref="inputheight"
              v-model="form.height"
              required
              placeholder="42"
              :state="v$.form.height.$dirty ? !v$.form.height.$error : null"
              type="number"
              description="In mm"
            />
            <div v-if="!v$.form.height.required" class="invalid-feedback d-block">
              Height is required
            </div>
          </b-form-group>

          <b-form-group id="input-group-template" label="Template" label-for="template">
            <b-form-textarea
              id="template"
              v-model="form.template"
              :state="v$.form.template.$dirty ? !v$.form.template.$error : null"
              rows="10"
              required
            />
          </b-form-group>

          <b-form-group id="input-group-text-template" label="Text Template" label-for="text-template">
            <b-form-textarea
              id="text-template"
              v-model="form.text_template"
              :state="v$.form.text_template.$dirty ? !v$.form.text_template.$error : null"
              rows="5"
              required
            />
          </b-form-group>

          <b-button type="submit" variant="primary">
            {{ labelTemplate == null ? 'Add' : 'Save' }}
          </b-button>

        &nbsp;&nbsp;&nbsp;&nbsp;

          <b-button
            v-if="labelTemplate && labelTemplate.id"
            variant="danger"
            @click="deleteLabelTemplate()"
          >
            Delete
          </b-button>
          <br><br>
        </b-form>
      </div>

      <div class="col-4">
        The template is a JSON as string, you can look at <a href="https://pdfme.com/docs/getting-started#sample-template" target="_blank">this doc</a> for the exact schema syntax.<br>
        Please note that, currently, only two elements can use substitutions.<br>
        The QrCode element needs to be called "qrcode", and the text one "text", the following list will show available substitutions.<br>
        You can add other fixed elements if wanted.<br><br><br>
        The following substitutions for the Text Template is available, depending if it's a Storage Location or Part:
        <ul>
          <li><code>{name}</code> Name of the element <small>(storage, part)</small></li>
          <li><code>{description}</code> Description of the element <small>(storage, part)</small></li>
          <li><code>{qrcode}</code> QrCode of the element <small>(storage, part)</small></li>
          <li><code>{category_name}</code> Name of the parent category (if any) of the element <small>(storage)</small></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import logger from '@/logging'
import apiService from '@/services/api/api.service'
import { mapState } from 'vuex'
import { required, maxLength, minValue } from '@vuelidate/validators'
import { useToast } from 'vue-toastification'
import ToastyToast from '@/components/toasty-toast'
import useVuelidate from '@vuelidate/core'

export default {
  name: 'LabelTemplatesList',
  components: {

  },
  data: () => ({
    labelTemplate: null,
    form: {
      id: null,
      name: '',
      height: 42,
      width: 69,
      template: '',
      text_template: ''
    }
  }),
  setup () {
    const toast = useToast()
    const v$ = useVuelidate()
    return { toast, v$ }
  },
  validations: {
    form: {
      name: { required, maxLength: maxLength(255) },
      height: {
        required,
        minValue: minValue(0)
      },
      width: {
        required,
        minValue: minValue(0)
      },
      template: { required },
      text_template: { required }
    }
  },
  computed: {
    ...mapState({
      labelTemplates: (state) => state.preloads.label_templates
    })
  },
  created () {
    this.fetchLabelTemplates(true)
  },
  methods: {
    fetchLabelTemplates (init = false) {
      if (!init) {
        apiService.getLabelTemplates()
          .then((res) => {
            this.$store.commit('setLabelTemplates', res.data)
            logger.default.info('Label templates reloaded')
          })
      }
    },
    switchToTab (lt) {
      this.labelTemplate = lt
      this.form.id = lt ? lt.id : null
      this.form.name = lt ? lt.name : ''
      this.form.width = lt ? lt.width : 69
      this.form.height = lt ? lt.height : 42
      this.form.template = lt ? lt.template : ''
      this.form.text_template = lt ? lt.text_template : ''
    },
    save () {
      this.v$.$touch()
      if (this.v$.$invalid) {
        logger.default.error('form has errors')
        return
      }

      let lt = {
        name: this.form.name,
        width: this.form.width,
        height: this.form.height,
        template: this.form.template,
        text_template: this.form.text_template
      }

      if (this.labelTemplate) {
        // update
        apiService.updateLabelTemplate(this.form.id, lt)
          .then(() => {
            this.toast.success({
              component: ToastyToast,
              props: {
                title: this.$pgettext('LabelTemplate/Update/Toast/Success/Title', 'Update label template'),
                message: this.$pgettext('LabelTemplate/Update/Toast/Success/Message', 'Success')
              }
            })
            this.switchToTab(null)
            this.fetchLabelTemplates()
          })
          .catch((error) => {
            this.toast.error({
              component: ToastyToast,
              props: {
                title: this.$pgettext('LabelTemplate/Update/Toast/Error/Title', 'Update label template'),
                message: this.$pgettext('LabelTemplate/Update/Toast/Error/Message', 'An error occured, please try again later')
              }
            })
            logger.default.error('Cannot update label template', error.message)
          })
      } else {
        // create
        apiService.createLabelTemplate(lt)
          .then(() => {
            this.toast.success({
              component: ToastyToast,
              props: {
                title: this.$pgettext('LabelTemplate/Add/Toast/Success/Title', 'Add label template'),
                message: this.$pgettext('LabelTemplate/Add/Toast/Success/Message', 'Success')
              }
            })
            this.switchToTab(null)
            this.fetchLabelTemplates()
          })
          .catch((error) => {
            this.toast.error({
              component: ToastyToast,
              props: {
                title: this.$pgettext('LabelTemplate/Add/Toast/Error/Title', 'Add label template'),
                message: this.$pgettext('LabelTemplate/Add/Toast/Error/Message', 'An error occured, please try again later')
              }
            })
            logger.default.error('Cannot add label template', error.message)
          })
      }
    },
    deleteLabelTemplate () {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the template '${this.form.name}' ?`, {
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
            apiService.deleteLabelTemplate(this.form.id)
              .then((val) => {
                this.toast.success({
                  component: ToastyToast,
                  props: {
                    title: this.$pgettext('LabelTemplate/Delete/Toast/Success/Title', 'Deleting label template'),
                    message: this.$pgettext('LabelTemplate/Delete/Toast/Success/Message', 'Success')
                  }
                })
                this.$nextTick(() => {
                  this.switchToTab(null)
                  this.fetchLabelTemplates()
                })
              })
              .catch((err) => {
                this.toast.error({
                  component: ToastyToast,
                  props: {
                    title: this.$pgettext('LabelTemplate/Delete/Toast/Error/Title', 'Deleting label template'),
                    message: this.$pgettext('LabelTemplate/Delete/Toast/Error/Message', 'An error occured, please try again later')
                  }
                })
                logger.default.error('Error with label template deletion', err)
                this.switchToTab(null)
                this.fetchLabelTemplates()
              })
          }
        })
    }
  }
}
</script>
