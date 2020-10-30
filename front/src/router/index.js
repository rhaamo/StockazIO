import LoginForm from '../components/login_form/login_form.vue'

import PartsAddFull from '../views/parts/AddFull'
import PartsAddQuick from '../views/parts/AddQuick'
import PartsList from '../views/parts/List'
import PartsDetails from '../views/parts/Details'
import ViewInfos from '../views/view/Infos'
import PartUnitsList from '../views/PartUnit/List'

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
    // PartUnits
    {
      path: '/part_units',
      name: 'part-units-list',
      component: PartUnitsList,
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
