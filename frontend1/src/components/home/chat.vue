<template>
  <footer id="bottom-tab-region">
    <div class="input-section">
      <input type="text" placeholder="Input here..." />
      <button class="send-btn">
        <img src="@/components/home/content/assets/send_msg.png" />
      </button>
    </div>
  </footer>
</template>

<script setup></script>

<style scoped lang="scss">
#bottom-tab-region {
  width: 100%;
  .input-section {
    display: flex;
    align-items: center;
    justify-content: center;
    input {
      font-family: "Noto Sans TC-Bold", Helvetica;
      width: 100px;
      border: none;
      border-width: 0px;
      border-bottom: 2px solid #A5C2BB;
      outline: none;
      padding: 10px;
      border-radius: 4px;
      margin-right: 10px;
      width: calc(100% - 800px);
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
