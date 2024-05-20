<template>
  <div id="home-root">
    <TopTabRegion id="top-tab-region" />
    <div class="content-region">
      <TabHome :messenges="messenges" v-show="selectedTabIndex == 0" />
    </div>
    <footer><BottomTabRegion @send-messenges="handleSendMessenge" id="bottom-tab-region" /></footer>
  </div>
  <!-- <Content/> -->
</template>

<script setup>
import TopTabRegion from "@/components/home/TopTabRegion.vue";
import TabHome from "@/components/home/content/TabHome.vue";
import BottomTabRegion from "@/components/home/BottomTabRegion.vue";
import { ref, onMounted,onUnmounted } from "vue";

const selectedTabIndex = ref(0);

const messenges = ref([])
function handleSendMessenge(newMessenge){
  messenges.value.push(newMessenge);
  console.log(messenges.value[0])
}

</script>

<style scoped lang="scss">
#home-root {
  width: 100%;
  height: 100%;

  #top-tab-region {
    background-color: blue;
    height: 100px;
    width: 100%;
  }

  #bottom-tab-region{
    // background-color: yellow ;
    // height: -80%;
    width: 100%;
  }
  .content-region {
    //background-color: blue ;
    width: 100%;
    height: calc(100% - 200px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: end;
    // position: absolute;
    overflow: scroll;
    // flex: 1;
    // overflow-y: auto;
  }
}
</style>