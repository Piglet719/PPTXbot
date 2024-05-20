<template>
  <div v-show="contentType == 2" class="Reupload-section">
    <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
    請選擇是否要匯入PPT模板
    <div class="actions">
      <button class="action-btn" @click="changeContentType(3)">Yes</button>
      <button class="action-btn" @click="changeContentType(3)">No</button>
    </div>
    <button class="pdf-input" @click="changeContentType(0)">
      重新匯入PDF
    </button>
  </div>

  <div v-show="contentType == 3" class="Reupload-section">
    <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
    請選擇/輸入要輸出的頁面
    <div class="actions">
      <button class="action-btn" @click="changeContentType(4)">Introduction</button>
      <button class="action-btn" @click="changeContentType(4)">Related Work</button>
      <button class="action-btn" @click="changeContentType(4)">Methdology</button>
      <button class="action-btn" @click="changeContentType(4)">Conclusion</button>
    </div>
    <button class="pdf-input" @click="changeContentType(0)">
      重新匯入PDF
    </button>
  </div>

  <div v-show="contentType == 4" class="Reupload-section">
    <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
    已轉檔完成！
    <div class="actions">
      <button class="download-btn">下載Power Point</button>
    </div>
    <button class="pdf-input" @click="changeContentType(0)">
      重新匯入PDF
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const contentType = ref(0);

function changeContentType(type) {
  contentType.value = type;
}
</script>

<style scoped lang="scss">
.Reupload-section {
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

.actions {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  .action-btn {
    background-color: white;
    border: 1px solid white;
    padding: 10px 20px;
    cursor: pointer;
    margin: 0 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 4px;
  }
}

.download-btn {
  background-color: #91c5b5;
  border: 1px solid white;
  padding: 10px 20px;
  cursor: pointer;
  margin: 0 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}
</style>