import LoginForm from '../components/login_form/login_form.vue'

import AddPart from '../views/AddPart'
import ViewInfos from '../views/view/Infos'

export default (store) => {
  const validateAuthenticatedRoute = (to, from, next) => {
    if (store.state.oauth.loggedIn) {
      next()
    } else {
      next('/login')
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
      component: AddPart,
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
