<template>
  <div v-show="contentType === 0" class="upload-section">
    <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
    請匯入論文PDF完整檔案
    <input type="file" @change="handleFileUpload" ref="fileInput" style="display: none;" />
    <button class="pdf-input" @click="triggerFileInput">
      匯入 PDF
    </button>
  </div>

  <div v-show="contentType === 1" class="outside-Reupload-section">
    <div class="Reupload-section">
      <div class="robot-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        資料分析中......
      </div>
    </div>
    <button class="pdf-input" @click="emitChangeContentType(2)">
      重新匯入PDF
    </button>
  </div>

  <div v-show="contentType === 2">
    <div class="Reupload-section">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      請選擇是否要匯入PPT模板
    </div>
    <div class="actions">
      <input type="file" ref="pptInput" @change="handlePPTUpload" style="display: none" />
      <button class="action-btn" @click="triggerPPTInput">
        Yes(ppt/pptx)
      </button>
      <button class="action-btn" @click="emitChangeContentType(3)">
        No
      </button>
    </div>
    <button class="pdf-input" @click="emitChangeContentType(0)">
      重新匯入PDF
    </button>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import axios from 'axios';

const props = defineProps({
  contentType: Number
});

const emit = defineEmits(['changeContentType']);

const fileInput = ref(null);
const pptInput = ref(null);

const triggerFileInput = () => {
  fileInput.value.click();
};

const triggerPPTInput = () => {
  pptInput.value.click();
};

const handleFileUpload = async () => {
  const file = fileInput.value.files[0];
  console.log(file);
  if (file && file.type === 'application/pdf') {
    emitChangeContentType(1);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post('http://localhost:8080/api/upload_file', formData);
      console.log(response.data);
      emitChangeContentType(2);
    } catch (error) {
      console.error('文件上傳失敗', error);
      alert('文件上傳失敗');
    }
  } else {
    alert('請選擇一個PDF文件');
  }
};

const handlePPTUpload = async () => {
  const file = pptInput.value.files[0];
  console.log(file);
  const validTypes = [
    'application/vnd.ms-powerpoint', // PPT
    'application/vnd.openxmlformats-officedocument.presentationml.presentation' // PPTX
  ];
  if (file && validTypes.includes(file.type)) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post('http://localhost:8080/api/upload_file', formData);
      console.log(response.data);
      emitChangeContentType(3);
    } catch (error) {
      console.error('文件上傳失敗', error);
      alert('文件上傳失敗');
    }
  } else {
    alert('請選擇一個PPT文件');
  }
};

const emitChangeContentType = (type) => {
  console.log(`Changing content type to ${type}`);
  emit('changeContentType', type);
};
</script>

<style scoped lang="scss">
.upload-section {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #FFFFFF;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 15px;
}

.robot-img {
  height: 30px;
  padding: 10px 10px 10px 10px;
}

.pdf-input {
  background-color: #4285f4;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  margin-left: 500px;
  display: flex;
  align-items: center;
  border-radius: 10;
  font-size: 15px;
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
  font-size: 15px;
}

.ouside-Reupload-section {
  background-color: green;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 15px;
  width: calc(100% - 500px);
}

.robot-section {
  display: flex;
  align-items: center;
  justify-content: center;
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

</style>
