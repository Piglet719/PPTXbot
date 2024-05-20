<template>
  <div v-show="contentType == 0" class="upload-section">
    <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
    請匯入論文PDF完整檔案
    <input type="file" @change="handleFileUpload" ref="fileInput" style="display: none;" />
    <button class="pdf-input" @click="triggerFileInput">
      匯入 PDF
    </button>
  </div>

  <div v-show="contentType == 1" class="outside-Reupload-section">
    <div class="Reupload-section">
      <div class="robot-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        資料分析中......
      </div>
    </div>
    <button class="pdf-input" @click="changeContentType(2)">
      重新匯入PDF
    </button>
  </div>
</template>

<script setup>
import { ref, watch, defineProps } from 'vue';

const props = defineProps({
  changeContentType: {
    type: Function,
    required: true,
  },
});

const contentType = ref(0);
const fileInput = ref(null);

watch(() => contentType.value, (newValue) => {
  if (newValue === 1) {
    // Mock analysis delay
    setTimeout(() => props.changeContentType(2), 2000);
  }
});

function triggerFileInput() {
  fileInput.value.click();
}

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (file) {
    console.log('File selected:', file);
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
      method: 'POST',
      body: formData,
    }).then(response => {
      if (response.ok) {
        // Record file information here if needed
        console.log('File uploaded successfully:', file);

        // Change the content type to indicate file upload success
        props.changeContentType(1);
      } else {
        console.error('File upload failed');
      }
    }).catch(error => {
      console.error('Error uploading file:', error);
    });
  }
}
</script>

<style scoped lang="scss">
.upload-section,
.Reupload-section,
.outside-Reupload-section {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 10px;
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
  font-size: 10px;
}

.robot-section {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
