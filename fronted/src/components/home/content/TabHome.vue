<template>
<!-- <div class="messenge-section"> -->
  <div class="messenge-section">
    <div class="onemessenge" v-for="(message, index) in messenges" :key="index">
      {{ message }}
    </div>
  </div>
<!-- </div> -->
  
  <div class="upload-section" v-show="contentType == 0">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      請匯入論文PDF完整檔案
    <!-- <button class="pdf-input" @click="changeContentType(1)"> -->
      <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none" />
      <button class="pdf-input" @click="triggerFileInput">
      匯入 PDF
    </button>
  </div>

  <div class="outside-Reupload-section" v-show="contentType == 1">
  <div class="Reupload-section">
    <div class="robot-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        資料分析中......
    </div>
  </div>
    <button class="pdf-input" @click="changeContentType(2)">
        重新匯入PDF
    </button>
  <!-- </div> -->
</div>

  <div v-show="contentType == 2">
    <div class="Reupload-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        請選擇是否要匯入PPT模板
    </div>
    <div class="actions">
          <input type="file" ref="pptInput" @change="handlePPTUpload" style="display: none" />
          <button class="action-btn" @click="triggerPPTInput">Yes(ppt/pptx)</button>
          <button class="action-btn" @click="changeContentType(3)">No</button>
    </div>
    <button class="pdf-input" @click="changeContentType(0,messenges)">
        重新匯入PDF
    </button>
  </div>

  <div v-show="contentType == 3">
    <div class="Reupload-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        請選擇/輸入要輸出的頁面
    </div>
    <div class="actions">
      <div v-for="option in options" :key="option.value">
      <button class="action-btn">
        <input type="checkbox" :value="option.value" v-model="selectedOptions" />
        {{ option.label }}
      </button>
    </div>
          <!-- <button class="action-btn" @click="changeContentType(4)">Introduction</button>
          <button class="action-btn" @click="changeContentType(4)">Related Work</button>
          <button class="action-btn" @click="changeContentType(4)">Methdology</button>
          <button class="action-btn" @click="changeContentType(4)">Conclusion</button> -->
        </div>
    <!-- <button class="send-btn" @click="changeContentType(4)" >
    </button> -->
    <button class="pdf-input" @click="changeContentType(0)">
        重新匯入PDF
    </button>
  </div>

  <div v-show="contentType == 4">
    <div class="Reupload-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        已轉檔完成！
    </div>
    <div class="actions">
          <button class="download-btn">下載Power Point</button>
        </div>
    <button class="pdf-input" @click="changeContentType(0)">
        重新匯入PDF
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, inject, defineProps } from "vue";
// import func from "../../../../../vue-temp/vue-editor-bridge";
const contentType = ref(0);
const sendMessenge = ref("");
const fileInput = ref(null);
const pptInput = ref(null);
const uploading = ref(false);
const pptFenerated = ref(false);
const options = [
  { value: 'option1', label: 'Introduction' },
  { value: 'option2', label: 'Related Work' },
  { value: 'option3', label: 'Methdology' },
  { value: 'option4', label: 'Conclusion' }
];


function changeContentType(type,messenges) {
  //轉換登入和註冊頁面
  contentType.value = type;
}

const props = defineProps({
  messenges:{
    type: Array,
    required:true
  }
});

const triggerFileInput = () => {
  fileInput.value.click();
  console.log(fileInput)
}

const triggerPPTInput = () => {
  pptInput.value.click();
}

const handleFileUpload = async () => {
  const file = fileInput.value.files[0];
  console.log(file)
  if (file && (file.type === 'application/pdf')) {
    contentType.value=1;
    // uploading.value = true;
    // pptGenerated.value = false;
    
    try {
      // 模擬文件上傳過程
      await new Promise(resolve => setTimeout(resolve, 2000)); // 模擬2秒上傳時間
      // pptGenerated.value = true;
      contentType.value=2;
    } catch (error) {
      console.error("文件上傳失敗", error);
    } finally {
      uploading.value = false;
    }
  } else {
    alert("請選擇一個PDF文件");
  }
};

const handlePPTUpload = async () => {
  const file = pptInput.value.files[0];
  console.log(file)
  const validTypes = [
    'application/vnd.ms-powerpoint', // PPT
    'application/vnd.openxmlformats-officedocument.presentationml.presentation' // PPTX
  ];
  if (file && validTypes.includes(file.type)) {
    // uploading.value = true;
    // pptGenerated.value = false;
    
    try {
      // 模擬文件上傳過程
      await new Promise(resolve => setTimeout(resolve, 2000)); // 模擬2秒上傳時間
      // pptGenerated.value = true;
      contentType.value=3;
    } catch (error) {
      console.error("文件上傳失敗", error);
    } finally {
      uploading.value = false;
    }
  }
  else {
    alert("請選擇一個PPT文件");
  }
};

function test(messenges){
  console.log(messenges)

}


// function sendMessenges(){
//   sendMessenge.value = 
// }
</script>

<style>
.upload-section {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color:#FFFFFF;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 10px;
  /* width: calc(100% - 400px); */
}

.messenge-section{
  width: calc(100%/2);
  transform: translate(40px,0);
  overflow-x: hidden;
  overflow-y: scroll;
  /* transform: translate(400px,0); */
  /* background-color: red; */
}
.onemessenge{
    display: flex;
    align-items: center;
    justify-content: right; 
    background-color: #ffffff;
    /* transform: translate(40px,0); */
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 10px;
    width: calc(100%-500px);
}
.robot-img{
  height: 30px;
  padding: 10px 10px 10px 10px;
}
.pdf-input{
  background-color: #4285F4;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  /* margin-right: 10px; */
  margin-left: 500px;
  display: flex;
  align-items: center;
  border-radius: 10;
  font-size: 10px;
}

.Reupload-section {
    display: flex;
    align-items: center;
    justify-content: left; 
    /* background-color: red; */
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 10px;
  }

  .ouside-Reupload-section {
    background-color: green;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 10px;
    width: calc(100% - 500px);
  }
  .robot-section{
    display: flex;
    align-items: center;
    justify-content: center;
    /* background-color: yellow; */
  }
  .actions {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
.action-btn {
  background-color: white;
  border: 1px solid white;
  padding: 10px 20px;
  cursor: pointer;
  margin: 0 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.download-btn {
  background-color: #91C5B5;
  border: 1px solid white;
  padding: 10px 20px;
  cursor: pointer;
  margin: 0 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

</style>
