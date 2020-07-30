<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header"> Change Password:
      </header>
        <section class="modal-body">
          <form v-on:submit.prevent=changePass>
              <label>Old Password:</label>
              <input type='password' v-bind:value="oldPass"
              v-on:input="oldPass = $event.target.value"/>
              <br />
              <label>New Password:</label>
              <input type='password' v-bind:value="newPass"
               v-on:input="newPass = $event.target.value"/>
              <br />
              <button type="submit">Change Password</button>
          </form>
          <span>{{warning}}</span>
        </section>
       <footer class="modal-footer">
        <button type="button" class="btn-green" @click="close">
            Close me!
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'changePasswordModal',
  data() {
    return {
      oldPass: '',
      newPass: '',
      warning: '',
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    changePass() {
      const path = 'http://localhost:5000/changePassword';
      const payload = JSON.parse(`{"username": "${localStorage.user}", "oldPassword": "${this.oldPass}", "newPassword": "${this.newPass}"}`);
      axios.post(path, payload).then((res) => {
        if (res.data.success) {
          this.warning = 'Password changed successfully!';
          setTimeout(() => { this.warning = ''; }, 5000);
          setTimeout(() => { this.close(); }, 5000);
        }
      }).catch((error) => {
        if (error) {
          this.warning = 'An error has occured. Was your old password correct?';
          setTimeout(() => { this.warning = ''; }, 2000);
        }
      });
    },
  },
};
</script>

<style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background: #FFFFFF;
    box-shadow: 2px 2px 20px 1px;
    overflow-x: auto;
    display: flex;
    flex-direction: column;
  }

  .modal-header,
  .modal-footer {
    padding: 15px;
    display: flex;
  }

  .modal-header {
    border-bottom: 1px solid #eeeeee;
    color: #4AAE9B;
    justify-content: space-between;
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    justify-content: flex-end;
  }

  .modal-body {
    position: relative;
    padding: 20px 10px;
  }

  .btn-green {
    color: white;
    background: #4AAE9B;
    border: 1px solid #4AAE9B;
    border-radius: 2px;
  }
</style>
