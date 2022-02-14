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
          <template v-if="items && items.length == 1">
            <template v-if="items[0].category">
              Storage location infos:<br>
              <ul>
                <li>Name: {{ items[0].name }}</li>
                <li>Description: {{ items[0].description || 'none' }}</li>
                <li>UUID: {{ items[0].uuid }}</li>
                <li>qrCode content: {{ qrCodeUri(items[0]) }}</li>
              </ul>
            </template>
            <template v-else>
              Part infos:<br>
              <ul>
                <li>Name: {{ items[0].name }}</li>
                <li>Description: {{ items[0].description || 'none' }}</li>
                <li>UUID: {{ items[0].uuid }}</li>
                <li>qrCode content: {{ qrCodeUri(items[0]) }}</li>
              </ul>
            </template>
          </template>
          <template v-else>
            Multiple items choosen for label generation.
            <ul>
              <li v-for="item in items" :key="item.id">{{ item.name }}</li>
            </ul>
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
          <br><br>
          <hr>
          You can use the PDF on the right to print corresponding labels.<br>
          Do not hesitate to download the PDF and open it natively if the print preview is showing a bad layout.
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
    items: {
      type: Array
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
    })
  },
  methods: {
    doSubstitutions (item) {
      let text = this.template.tpl.text_template
      text = item && item.name ? text.replace('{name}', item.name) : text
      text = item && item.description ? text.replace('{description}', item.description) : text.replace('{description}', '') // description is optional
      text = item && item.uuid ? text.replace('{qrcode}', this.qrCodeUri(item)) : text
      return text
    },
    qrCodeUri (item) {
      if (item.category) {
        // location
        return `web+stockazio:storageLocation,${item.uuid}`
      } else {
        // part
        return `web+stockazio:part,${item.uuid}`
      }
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
        'qrcode': this.qrCodeUri(this.items[0]),
        'text': this.doSubstitutions(this.items[0])
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
