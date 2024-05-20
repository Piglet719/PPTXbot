<template>
  <div id="home-root">
    <div id="top-tab-region">
      <img class="logo" src="@/components/home/content/assets/logo.png" alt="Power Paper Logo"/>
      <span class="title">Power Paper : 死線戰士小幫手</span>
      <div class="diamod">
        <div>wowowowo</div>
      </div>
    </div>
    <div class="content-region">
      <div v-show="selectedTabIndex == 0">
        <upload-file :changeContentType="changeContentType" />
        <create-ppt :changeContentType="changeContentType" :contentType="contentType" />
      </div>
    </div>
    <chat />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import UploadFile from './upload_file.vue';
import CreatePPT from './create_ppt.vue';
import Chat from './chat.vue';

const selectedTabIndex = ref(0);
const contentType = ref(0);

function changeContentType(type) {
  contentType.value = type;
}
</script>

<style scoped lang="scss">
#home-root {
  width: 100%;
  height: 100%;

  #top-tab-region {
    background-color: #A5C2BB;
    height: 100px;
    width: 100%;
    .logo {
      height: 45px;
    }
    .title {
      color: var(--textprimarygrey-1);
      font-family: "Noto Sans TC-Bold", Helvetica;
      font-weight: 800;
      font-size: 15px;
      padding: 5px 10px 10px 5px;
    }
    .diamod {
      left: 50%;
      display: inline-block;
      height: 70px;
      width: 100%;
      color: #A5C2BB;
      background: #A5C2BB;
    }
  }

  .content-region {
    width: 100%;
    height: calc(100% - 200px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: end;
  }
}
</style>
