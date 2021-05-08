import LoginForm from '../components/login_form/login_form.vue'

import PartsAddFull from '../views/parts/AddFull'
import PartsAddQuick from '../views/parts/AddQuick'
import PartsList from '../views/parts/List'
import PartsDetails from '../views/parts/Details'
import PartsEdit from '../views/parts/Edit'
import ViewInfos from '../views/view/Infos'
import ViewStorageTree from '../views/view/StorageTree'
import PartUnitsList from '../views/PartUnit/List'
import ParametersUnitsList from '../views/ParametersUnits'
import ParametersPresetsList from '../views/ParametersPresets/list'
import Distributors from '../views/Distributors'
import Manufacturers from '../views/Manufacturers'
import OrdersImporter from '../views/view/OrdersImporter'
import OrdersImporterDetails from '../views/view/OrdersImporterDetails'
import OrdersCategoryMatchers from '../views/view/OrdersCategoryMatchers'
import PublicPartsList from '../views/view/public/PartsList'
import ProjectsList from '../views/projects/list'
import ProjectsAdd from '../views/projects/add'
import ProjectsEdit from '../views/projects/edit'
import ProjectsDetails from '../views/projects/details'

export default (store) => {
  const validateAuthenticatedRoute = (to, from, next) => {
    if (store.state.oauth.loggedIn) {
      next()
    } else {
      next('/')
    }
  }

  return [
    // Main stuff
    {
      path: '/',
      name: 'home',
      redirect: _to => { return (store.state.oauth.loggedIn ? '/parts' : '/login') }
    },
    // Parts
    {
      path: '/parts/new',
      name: 'parts-new',
      component: PartsAddFull,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/parts/quick-new',
      name: 'parts-quick-new',
      component: PartsAddQuick,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/parts/category/:categoryId',
      name: 'parts-category-list',
      component: PartsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/parts',
      name: 'parts-list',
      component: PartsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/parts/:partId',
      name: 'parts-details',
      component: PartsDetails,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/parts/:partId/edit',
      name: 'parts-edit',
      component: PartsEdit,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    // PartUnits
    {
      path: '/part/units',
      name: 'part-units-list',
      component: PartUnitsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    // Parameters Units
    {
      path: '/part/parameters/units',
      name: 'parameters-units-list',
      component: ParametersUnitsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    // Parameters Presets
    {
      path: '/part/parameters/presets',
      name: 'parameters-presets-list',
      component: ParametersPresetsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    // Distributors
    {
      path: '/distributors',
      name: 'distributors-list',
      component: Distributors,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    // Manufacturers
    {
      path: '/manufacturers',
      name: 'manufacturers-list',
      component: Manufacturers,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    // Views
    {
      path: '/view/infos',
      name: 'view-infos',
      component: ViewInfos,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/views/storage-tree',
      name: 'view-storage-tree',
      component: ViewStorageTree,
      beforeEnter: validateAuthenticatedRoute
    },
    // OrdersImporter
    {
      // this one needs to be before orders-importer-details for props reasons
      path: '/orders/importer/category_matcher',
      name: 'orders-importer-category-matcher',
      component: OrdersCategoryMatchers,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/orders/importer',
      name: 'orders-importer',
      component: OrdersImporter,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/orders/importer/:id',
      name: 'orders-importer-details',
      component: OrdersImporterDetails,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    // Public
    {
      path: '/public/parts',
      name: 'public-parts',
      component: PublicPartsList,
      props: true
    },
    {
      path: '/public/parts/category/:categoryId',
      name: 'public-parts-category-list',
      component: PublicPartsList,
      props: true
    },
    // Projects
    {
      path: '/projects',
      name: 'projects-list',
      component: ProjectsList,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/projects/new',
      name: 'projects-new',
      component: ProjectsAdd,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/projects/:projectId/edit',
      name: 'projects-edit',
      component: ProjectsEdit,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    {
      path: '/projects/:projectId',
      name: 'projects-details',
      component: ProjectsDetails,
      props: true,
      beforeEnter: validateAuthenticatedRoute
    },
    // Other
    {
      path: '/about',
      name: 'about',
      component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    // Auth
    { path: '/login', name: 'login_form', component: LoginForm },
    { name: 'password-reset', path: '/password-reset' },
    // Parts
    { path: '/parts', name: 'parts', beforeEnter: validateAuthenticatedRoute }
  ]
}
