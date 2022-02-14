<template>
  <b-modal
    id="modalLabelGenerator" ref="modalLabelGenerator"
    size="xl" hide-footer
    @show="modalLabelGeneratorShow"
    @cancel="modalLabelGeneratorClose"
    @close="modalLabelGeneratorClose" @hidden="modalLabelGeneratorClose"
  >
    <template #modal-header="{ close }">
      <h5 id="modalPartTitle">
        QrCode Label Generator
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
        <div class="col-md-5 mx-auto">
          <template v-if="item">
            <template v-if="item.category">
              Storage location infos:<br>
              <ul>
                <li>Name: {{ item.name }}</li>
                <li>Description: {{ item.description || 'none' }}</li>
                <li>UUID: {{ item.uuid }}</li>
                <li>qrCode content: {{ qrCodeUri }}</li>
              </ul>
            </template>
            <template v-else>
              Part infos:<br>
              <ul>
                <li>Name: {{ item.name }}</li>
                <li>Description: {{ item.description || 'none' }}</li>
                <li>UUID: {{ item.uuid }}</li>
                <li>qrCode content: {{ qrCodeUri }}</li>
              </ul>
            </template>
          </template>
          <br><br>
          <b-form-group id="input-group-template" label="Template:" label-for="template">
            <vue-multiselect
              v-model="template" :options="labelTemplates"
              placeholder="Please select a template"
              label="name" track-by="tpl"
              :allow-empty="false" deselect-label="Cannot remove this item"
              @select="templateChanged"
            />
          </b-form-group>
        </div>
        <div class="col-md-7 mx-auto">
          <vue-pdf-app
            v-if="pdf" :pdf="pdf" :config="pdfJsConfig"
            style="min-height: 30em;"
          />
        </div>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { generate } from '@pdfme/generator'
import VuePdfApp from 'vue-pdf-app'
import 'vue-pdf-app/dist/icons/main.css'
import { mapState } from 'vuex'

export default {
  components: {
    VuePdfApp
  },
  props: {
    item: {
      type: Object
    }
  },
  data: () => ({
    template: null,
    pdf: null,
    pdfJsConfig: {
      sidebar: false,
      secondaryToolbar: {
        secondaryPresentationMode: true,
        secondaryOpenFile: true,
        secondaryPrint: true,
        secondaryDownload: true,
        secondaryViewBookmark: true,
        firstPage: true,
        lastPage: true,
        pageRotateCw: true,
        pageRotateCcw: true,
        cursorSelectTool: true,
        cursorHandTool: true,
        scrollVertical: true,
        scrollHorizontal: true,
        scrollWrapped: true,
        spreadNone: false,
        spreadOdd: false,
        spreadEven: false,
        documentProperties: false
      },
      toolbar: {
        toolbarViewerLeft: {
          findbar: false,
          previous: true,
          next: true,
          pageNumber: true
        },
        toolbarViewerRight: {
          presentationMode: false,
          openFile: false,
          print: true,
          download: true,
          viewBookmark: false
        },
        toolbarViewerMiddle: {
          zoomOut: true,
          zoomIn: true,
          scaleSelectContainer: true
        }
      },
      errorWrapper: true
    }
  }),
  computed: {
    ...mapState({
      labelTemplates: (state) => {
        return state.preloads.label_templates.map(x => { return { name: x.name, tpl: x } })
      }
    }),
    qrCodeUri: function () {
      if (this.item.category) {
        // location
        return `web+stockazio:storageLocation,${this.item.uuid}`
      } else {
        // part
        return `web+stockazio:part,${this.item.uuid}`
      }
    }
  },
  methods: {
    doSubstitutions () {
      let text = this.template.tpl.text_template
      text = this.item && this.item.name ? text.replace('{name}', this.item.name) : text
      text = this.item && this.item.description ? text.replace('{description}', this.item.description) : text.replace('{description}', '') // description is optional
      text = this.item && this.item.uuid ? text.replace('{qrcode}', this.qrCodeUri) : text
      return text
    },
    modalLabelGeneratorShow () {
      // Auto select the first one
      this.template = this.labelTemplates && this.labelTemplates.length ? this.labelTemplates[0] : null
      this.generatePdf()
    },
    modalLabelGeneratorClose () {
      this.template = null
      this.pdf = null
    },
    templateChanged (item) {
      // We need to wait next tick or we get a delay in change of this.template
      this.$nextTick(() => {
        this.generatePdf()
      })
    },
    generatePdf () {
      const template = {
        basePdf: this.template.tpl.base_pdf,
        schemas: [
          JSON.parse(this.template.tpl.template)
        ]
      }
      let inputs = [{
        'qrcode': this.qrCodeUri,
        'text': this.doSubstitutions()
      }]
      generate({ template, inputs })
        .then((pdf) => {
          let blob = new Blob([pdf.buffer], { type: 'application/pdf' })
          this.pdf = URL.createObjectURL(blob)
        })
    }
  }
}
</script>

<style>
</style>
