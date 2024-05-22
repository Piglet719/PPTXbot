<template>
  <div id="home-root">
    <div id="top-tab-region">
      <div class="form-control">
        <img class="logo" src="@/components/home/content/assets/logo.png" alt="Power Paper Logo"/>
        <span class="title">Power Paper : 死線戰士小幫手</span>
      </div>
    </div>

    <div class="content-region">
      <Chat :messenges="messenges" @sendMessenges="handleSendMessenge" />
      <div v-show="selectedTabIndex == 0">
        <UploadFile :contentType="contentType" @changeContentType="changeContentType" />
        <CreatePPT :contentType="contentType" @hangeContentType="changeContentType" />
      </div>
      <button class="file-bottom" @click="showFileList">顯示已上傳檔案</button>
      <FileList v-if="showFileListFlag" :fileList="fileList"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Chat from './chat.vue';
import UploadFile from './upload_file.vue';
import CreatePPT from './create_ppt.vue';
import FileList from './file_list.vue';

const fileList = [
  { name: "example.pdf", type: "pdf", path: "C:/Users/Sunny/download/itor2006.pdf" },
  { name: "example1.pdf", type: "pdf", path: "C:/Users/Sunny/download/IP.pdf" },
  { name: "example2.pdf", type: "pdf", path: "C:/Users/Sunny/download/CAIE2021.pdf" },
  { name: "example.pptx", type: "ppt", path: "C:/Users/Sunny/download/CA_HW3.pptx" },
  { name: "example1.pptx", type: "ppt", path: "C:/Users/Sunny/download/motionGraph.pptx" },
  { name: "example2.pptx", type: "ppt", path: "C:/Users/Sunny/download/ProjectProposal.pptx" }
];

const selectedTabIndex = ref(0);
const messenges = ref([]);
const contentType = ref(0);
const showFileListFlag = ref(false);

function changeContentType(type) {
  contentType.value = type;
}

function handleSendMessenge(newMessenge){
  messenges.value.push(newMessenge);
  console.log(messenges.value[0])
}

function showFileList() {
  showFileListFlag.value = !showFileListFlag.value;
}

</script>

<style scoped lang="scss">
#home-root {
  width: 100%;
  height: 100%;
  
  #top-tab-region {
    background-color: #A5C2BB;
    height: 70px;
    width: 100%;
    .logo {
      height: 50px;
    }
    .title {
      color: var(--textprimarygrey-1);
      font-family: "Noto Sans TC-Bold", Helvetica;
      font-weight: 800;
      font-size: 15px;
      padding: 5px 10px 10px 5px;
    }
    
    .form-control {
        position: relative;
        margin-top: 5px;
        margin-left: 10px;
    }
  }

  .content-region {
    width: 100%;
    height: calc(100% - 170px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: end;
  }
  
  #bottom-tab-region {
  width: 100%;
  }
}

.file-bottom {
  background-color: #4285f4;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  margin-middle: 100px;
  display: flex;
  align-items: center;
  border-radius: 10;
  font-size: 10px;
}

</style>
