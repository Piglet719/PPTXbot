import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'

import router from './router'

const app = createApp(App)
// const top = createApp(main)
// const text1 = createApp(maintext)
// const text2 = createApp(maintext1)
// const text3 = createApp(maintext2)

app.use(createPinia())
app.use(router)
// top.use(router)
// text1.use(router)
// text2.use(router)
// text3.use(router)

app.mount('#app')
// top.mount('#main')
// text1.mount('#text1')
// text2.mount('#text2')
// text3.mount('#text3')


