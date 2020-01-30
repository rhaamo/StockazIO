import LoginForm from '../components/login_form/login_form.vue'

export default (store) => {
  const validateAuthenticatedRoute = (to, from, next) => {
    if (store.state.user.currentUser) {
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
      redirect: _to => { return (store.state.user.currentUser ? '/parts' : '/login') }
    },
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
