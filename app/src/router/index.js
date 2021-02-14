import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/cooccurrences",
    name: "cooccurrences",
    component: () => import(/* webpackChunkName: "about" */ "../views/Cooccurrences.vue")
  },
  {
    path: "/genealogy",
    name: "genealogy",
    component: () => import(/* webpackChunkName: "about" */ "../views/Genealogy.vue")
  },
  {
    path: "/narrative",
    name: "narrative",
    component: () => import(/* webpackChunkName: "about" */ "../views/Narrative.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
