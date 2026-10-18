import ui from "@nuxt/ui/vue-plugin";
import { createApp } from "vue";
import "./assets/css/main.css";
import App from "./App.vue";
import { i18n } from "./i18n";
import { router } from "./router";

createApp(App).use(router).use(i18n).use(ui).mount("#app");
