import Axios from 'axios'
import fileDownload from 'js-file-download'

const CHECK_TOKEN_URL = '/oauth/check_token/'

const CATEGORIES_URL = '/api/v1/categories/'

const APP_INFORMATIONS_URL = '/api/v1/app/informations'

const FOOTPRINTS_URL = '/api/v1/footprints/'

const STORAGES_URL = '/api/v1/storages/'

const PARAMETERS_UNITS_URL = '/api/v1/parts/parameters/units/'
const PARAMETERS_UNITS_CREATE = '/api/v1/parts/parameters/units/'
const PARAMETERS_UNITS_DELETE = (id) => `/api/v1/parts/parameters/units/${id}/`
const PARAMETERS_UNITS_UPDATE = (id) => `/api/v1/parts/parameters/units/${id}/`

const PART_UNITS_URL = '/api/v1/parts/units/'
const PART_UNITS_CREATE = '/api/v1/parts/units/'
const PART_UNITS_DELETE = (partUnitId) => `/api/v1/parts/units/${partUnitId}/`
const PART_UNITS_UPDATE = (partUnitId) => `/api/v1/parts/units/${partUnitId}/`

const PART_PARAMETERS_PRESETS_URL = '/api/v1/parts/parameters/presets/'
const PART_PARAMETERS_PRESETS_CREATE = '/api/v1/parts/parameters/presets/'
const PART_PARAMETERS_PRESETS_DETAILS = (partParameterPresetId) => `/api/v1/parts/parameters/presets/${partParameterPresetId}/`
const PART_PARAMETERS_PRESETS_DELETE = (partParameterPresetId) => `/api/v1/parts/parameters/presets/${partParameterPresetId}/`
const PART_PARAMETERS_PRESETS_UPDATE = (partParameterPresetId) => `/api/v1/parts/parameters/presets/${partParameterPresetId}/`

const PARTS_CREATE = '/api/v1/parts/'
const PARTS_LIST = '/api/v1/parts/'
const PARTS_UPDATE = (id) => `/api/v1/parts/${id}/`
const PARTS_ITEM = (partId) => `/api/v1/parts/${partId}/`
const PARTS_ATTACHMENTS_CREATE = (partId) => `/api/v1/parts/${partId}/attachments/`
const PARTS_ATTACHMENTS_DELETE = (partId, pk) => `/api/v1/parts/${partId}/attachments/${pk}` // no final /

const PARTS_PUBLIC_LIST = '/api/v1/parts/public/'
const PARTS_PUBLIC_ITEM = (partId) => `/api/v1/parts/public/${partId}/`

const PARTS_AUTOCOMPLETE_QUICK = (name) => `/api/v1/parts/autocomplete/quick_by_name/${name}` // no final /

const MANUFACTURERS_URL = '/api/v1/manufacturers/'
const MANUFACTURERS_CREATE = '/api/v1/manufacturers/'
const MANUFACTURERS_DELETE = (id) => `/api/v1/manufacturers/${id}/`
const MANUFACTURERS_UPDATE = (id) => `/api/v1/manufacturers/${id}/`

const DISTRIBUTORS_URL = '/api/v1/distributors/'
const DISTRIBUTORS_CREATE = '/api/v1/distributors/'
const DISTRIBUTORS_DELETE = (id) => `/api/v1/distributors/${id}/`
const DISTRIBUTORS_UPDATE = (id) => `/api/v1/distributors/${id}/`

const ORDERS_IMPORTER_LIST = '/api/v1/orders_importer/'
const ORDERS_IMPORTER_DETAILS = (id) => `/api/v1/orders_importer/${id}/`
const ORDERS_IMPORTER_UPDATE = (id) => `/api/v1/orders_importer/${id}/`
const ORDERS_IMPORTER_TO_INVENTORY = '/api/v1/orders_importer/import_to_inventory' // no final /

const CATEGORIES_MATCHERS_LIST = '/api/v1/orders_importer/category_matcher/'
const CATEGORIES_MATCHERS_BATCH_UPDATE = '/api/v1/orders_importer/category_matcher/batch_update' // no final /
const CATEGORIES_MATCHERS_REMATCH = '/api/v1/orders_importer/category_matcher/rematch' // no final /

const PROJECTS_LIST = '/api/v1/projects/'
const PROJECT_CREATE = '/api/v1/projects/'
const PROJECT_GET = (id) => `/api/v1/projects/${id}/`
const PROJECT_UPDATE = (id) => `/api/v1/projects/${id}/`
const PROJECT_DELETE = (id) => `/api/v1/projects/${id}/`
const PROJECT_ATTACHMENTS_CREATE = (projectId) => `/api/v1/projects/${projectId}/attachments/`
const PROJECT_ATTACHMENTS_DELETE = (projectId, pk) => `/api/v1/projects/${projectId}/attachments/${pk}` // no final /
const PROJECT_PARTS_CREATE = (projectId) => `/api/v1/projects/${projectId}/parts/`
const PROJECT_PARTS_UPDATE = (projectId, pk) => `/api/v1/projects/${projectId}/parts/${pk}` // no final /
const PROJECT_PARTS_DELETE = (projectId, pk) => `/api/v1/projects/${projectId}/parts/${pk}` // no final /
const PROJECT_EXPORT_INFOS_TXT = (projectId) => `/api/v1/projects/${projectId}/exports/infos.txt`
const PROJECT_EXPORT_BOM_CSV = (projectId) => `/api/v1/projects/${projectId}/exports/bom.csv`
const PROJECT_EXPORT_BOM_XLSX = (projectId) => `/api/v1/projects/${projectId}/exports/bom.xlsx`

// Auth
const verifyCredentials = () => {
  return Axios.get(CHECK_TOKEN_URL)
}

// Categories

const getCategories = () => {
  return Axios.get(CATEGORIES_URL)
}

// Informations

const getInformations = () => {
  return Axios.get(APP_INFORMATIONS_URL)
}

// Footprints

const getFootprints = () => {
  return Axios.get(FOOTPRINTS_URL)
}

// Storages

const getStorages = () => {
  return Axios.get(STORAGES_URL)
}

// Parameters units

const getParametersUnits = () => {
  return Axios.get(PARAMETERS_UNITS_URL)
}

const createParametersUnits = (data) => {
  return Axios.post(PARAMETERS_UNITS_CREATE, data)
}

const deleteParametersUnits = (id) => {
  return Axios.delete(PARAMETERS_UNITS_DELETE(id))
}

const updateParametersUnits = (id, data) => {
  return Axios.put(PARAMETERS_UNITS_UPDATE(id), data)
}

// Part units

const getPartUnits = () => {
  return Axios.get(PART_UNITS_URL)
}

const createPartUnit = (data) => {
  return Axios.post(PART_UNITS_CREATE, data)
}

const deletePartUnit = (partUnitId) => {
  return Axios.delete(PART_UNITS_DELETE(partUnitId))
}

const updatePartUnit = (partUnitId, data) => {
  return Axios.put(PART_UNITS_UPDATE(partUnitId), data)
}

// Part parameters presets

const getPartParameterPresets = () => {
  return Axios.get(PART_PARAMETERS_PRESETS_URL)
}

const getPartParameterPreset = (partParameterPresetId) => {
  return Axios.get(PART_PARAMETERS_PRESETS_DETAILS(partParameterPresetId))
}

const createPartParameterPresets = (data) => {
  return Axios.post(PART_PARAMETERS_PRESETS_CREATE, data)
}

const deletePartParameterPresets = (partParameterPresetId) => {
  return Axios.delete(PART_PARAMETERS_PRESETS_DELETE(partParameterPresetId))
}

const updatePartParameterPresets = (partParameterPresetId, data) => {
  return Axios.put(PART_PARAMETERS_PRESETS_UPDATE(partParameterPresetId), data)
}

// Manufacturers

const getManufacturers = () => {
  return Axios.get(MANUFACTURERS_URL)
}

const createManufacturer = (data) => {
  let formData = new FormData()
  if (data.name) {
    formData.append('name', data.name)
  }
  if (data.address) {
    formData.append('address', data.address)
  }
  if (data.url) {
    formData.append('url', data.url)
  }
  if (data.email) {
    formData.append('email', data.email)
  }
  if (data.comment) {
    formData.append('comment', data.comment)
  }
  if (data.phone) {
    formData.append('phone', data.phone)
  }
  if (data.fax) {
    formData.append('fax', data.fax)
  }
  if (data.logo && data.logo instanceof File) {
    formData.append('logo', data.logo)
  }
  return Axios.post(MANUFACTURERS_CREATE, formData)
}

const updateManufacturer = (id, data) => {
  let formData = new FormData()
  if (data.name) {
    formData.append('name', data.name)
  }
  if (data.address) {
    formData.append('address', data.address)
  }
  if (data.url) {
    formData.append('url', data.url)
  }
  if (data.email) {
    formData.append('email', data.email)
  }
  if (data.comment) {
    formData.append('comment', data.comment)
  }
  if (data.phone) {
    formData.append('phone', data.phone)
  }
  if (data.fax) {
    formData.append('fax', data.fax)
  }
  if (data.logo && data.logo instanceof File) {
    formData.append('logo', data.logo)
  }
  return Axios.put(MANUFACTURERS_UPDATE(id), formData)
}

const deleteManufacturer = (id) => {
  return Axios.delete(MANUFACTURERS_DELETE(id))
}

// Distributors

const getDistributors = () => {
  return Axios.get(DISTRIBUTORS_URL)
}

const createDistributor = (data) => {
  return Axios.post(DISTRIBUTORS_CREATE, data)
}

const updateDistributor = (id, data) => {
  return Axios.put(DISTRIBUTORS_UPDATE(id), data)
}

const deleteDistributor = (id) => {
  return Axios.delete(DISTRIBUTORS_DELETE(id))
}

// Part

const createPart = (data) => {
  return Axios.post(PARTS_CREATE, data)
}

const updatePart = (id, data) => {
  return Axios.put(PARTS_UPDATE(id), data)
}

const updatePartialPart = (id, data) => {
  return Axios.patch(PARTS_UPDATE(id), data)
}

const getParts = (params) => {
  return Axios.get(PARTS_LIST, { params: params })
}

const getPart = (partId) => {
  return Axios.get(PARTS_ITEM(partId))
}

const deletePart = (partId) => {
  return Axios.delete(PARTS_ITEM(partId))
}

const partsAutocompleteQuick = (name) => {
  return Axios.get(PARTS_AUTOCOMPLETE_QUICK(name))
}

const getPublicParts = (params) => {
  return Axios.get(PARTS_PUBLIC_LIST, { params: params })
}

const getPublicPart = (partId) => {
  return Axios.get(PARTS_PUBLIC_ITEM(partId))
}

const partAttachmentCreate = (partId, data) => {
  let formData = new FormData()
  formData.append('file', data.file)
  formData.append('description', data.description)
  formData.append('part', data.part_id ? data.part_id : partId)
  return Axios.post(PARTS_ATTACHMENTS_CREATE(partId), formData)
}

const partAttachmentDelete = (partId, partAttachmentId) => {
  return Axios.delete(PARTS_ATTACHMENTS_DELETE(partId, partAttachmentId))
}

// Order Importer

const getOrderImporter = (id) => {
  return Axios.get(ORDERS_IMPORTER_DETAILS(id))
}

const updateOrderImporter = (id, data) => {
  return Axios.put(ORDERS_IMPORTER_UPDATE(id), data)
}

const updatePartialOrderImporter = (id, data) => {
  return Axios.patch(ORDERS_IMPORTER_UPDATE(id), data)
}

const getOrdersImporter = () => {
  return Axios.get(ORDERS_IMPORTER_LIST)
}

const importOrderToInventory = (id) => {
  return Axios.post(ORDERS_IMPORTER_TO_INVENTORY, { 'id': id })
}

const getCategoryMatchers = () => {
  return Axios.get(CATEGORIES_MATCHERS_LIST)
}

const updateCategoryMatchers = (data) => {
  return Axios.patch(CATEGORIES_MATCHERS_BATCH_UPDATE, data)
}

const rematchOrderItems = () => {
  return Axios.get(CATEGORIES_MATCHERS_REMATCH)
}

// Projects

const getProjects = (params) => {
  return Axios.get(PROJECTS_LIST, { params: params })
}

const getProject = (id) => {
  return Axios.get(PROJECT_GET(id))
}

const createProject = (data) => {
  return Axios.post(PROJECT_CREATE, data)
}

const updateProject = (id, data) => {
  return Axios.put(PROJECT_UPDATE(id), data)
}

const updatePartialProject = (id, data) => {
  return Axios.patch(PROJECT_UPDATE(id), data)
}

const deleteProject = (id) => {
  return Axios.delete(PROJECT_DELETE(id))
}

const projectAttachmentCreate = (projectId, data) => {
  let formData = new FormData()
  formData.append('file', data.file)
  formData.append('description', data.description)
  formData.append('project', data.project_id ? data.project_id : projectId)
  return Axios.post(PROJECT_ATTACHMENTS_CREATE(projectId), formData)
}

const projectAttachmentDelete = (projectId, partAttachmentId) => {
  return Axios.delete(PROJECT_ATTACHMENTS_DELETE(projectId, partAttachmentId))
}

const projectAddPart = (id, data) => {
  return Axios.post(PROJECT_PARTS_CREATE(id), data)
}

const projectDeletePart = (id, partId) => {
  return Axios.delete(PROJECT_PARTS_DELETE(id, partId))
}

const projectUpdatePart = (id, partId, data) => {
  return Axios.post(PROJECT_PARTS_UPDATE(id, partId), data)
}

const projectExportInfosTxt = (id, filename) => {
  return Axios.get(PROJECT_EXPORT_INFOS_TXT(id), {
    responseType: 'blob'
  })
    .then((res) => {
      fileDownload(res.data, filename)
    })
}

const projectExportBomCSV = (id, filename) => {
  return Axios.get(PROJECT_EXPORT_BOM_CSV(id), {
    responseType: 'blob'
  })
    .then((res) => {
      fileDownload(res.data, filename)
    })
}

const projectExportBomXLSX = (id, filename) => {
  return Axios.get(PROJECT_EXPORT_BOM_XLSX(id), {
    responseType: 'blob'
  })
    .then((res) => {
      fileDownload(res.data, filename)
    })
}

const apiService = {
  verifyCredentials,
  getCategories,
  getInformations,
  getFootprints,
  getStorages,
  getParametersUnits,
  createParametersUnits,
  deleteParametersUnits,
  updateParametersUnits,
  getPartUnits,
  createPartUnit,
  deletePartUnit,
  updatePartUnit,
  getPartParameterPresets,
  getPartParameterPreset,
  createPartParameterPresets,
  deletePartParameterPresets,
  updatePartParameterPresets,
  getManufacturers,
  createManufacturer,
  updateManufacturer,
  deleteManufacturer,
  getDistributors,
  createDistributor,
  updateDistributor,
  deleteDistributor,
  createPart,
  updatePart,
  updatePartialPart,
  getParts,
  getPart,
  deletePart,
  partsAutocompleteQuick,
  getPublicParts,
  getPublicPart,
  partAttachmentCreate,
  partAttachmentDelete,
  getOrdersImporter,
  getOrderImporter,
  importOrderToInventory,
  updateOrderImporter,
  updatePartialOrderImporter,
  getCategoryMatchers,
  updateCategoryMatchers,
  rematchOrderItems,
  getProjects,
  getProject,
  createProject,
  updateProject,
  updatePartialProject,
  deleteProject,
  projectAttachmentCreate,
  projectAttachmentDelete,
  projectAddPart,
  projectDeletePart,
  projectUpdatePart,
  projectExportInfosTxt,
  projectExportBomCSV,
  projectExportBomXLSX
}

export default apiService
