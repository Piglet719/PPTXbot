<template>
  <footer id="bottom-tab-region">
    <div class="input-section">
      <input v-model="message" type="text" placeholder="Input here..." @keyup.enter="sendMessenges" />
      <button class="send-btn" @click="sendMessenges">
        <img src="@/components/home/content/assets/send_msg.png" />
      </button>
    </div>
  </footer>

  <div class="messenge-section">
    <div class="onemessenge" v-for="(msg, index) in messenges" :key="index">
      {{ msg }}
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";

const props = defineProps({
  messenges: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(["sendMessenges"]);
const message = ref("");

function sendMessenges() {
  if (message.value.trim()) {
    const newMessage = message.value.trim();
    message.value = "";
    emit("sendMessenges", newMessage);
  }
}
</script>


<style scoped lang="scss">

.messenge-section {
  width: calc(100%/2);
  transform: translate(40px,0);
  overflow-x: hidden;
  overflow-y: scroll;
}

.onemessenge {
  display: flex;
  align-items: center;
  justify-content: left;
  background-color: #ffffff;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 15px;
  width: calc(100% - 5px);
}

#bottom-tab-region {
  width: 100%;
  
  .input-section {
    position: fixed; /* 固定位置 */
    bottom: 20px; /* 距離底部 20px */
    left: 50%; /* 從左側 50% */
    transform: translateX(-50%); /* 向左移動 50% 以居中 */
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%; /* 撑满整个宽度 */
    padding: 10px; /* 增加 padding 以便更好看 */

    
    input {
      font-family: "Noto Sans TC-Bold", Helvetica;
      width: 70%;
      border: none;
      border-bottom: 2px solid #A5C2BB;
      outline: none;
      padding: 10px;
      border-radius: 4px;
      margin-right: 10px;
    }

    .send-btn {
      border: none;
      background-color: white;
      cursor: pointer;
      img {
        height: 25px;
      }
    }
  }
}
</style>
