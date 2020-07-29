<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header" v-show="login">
          Login:
      </header>
      <header class="modal-header" v-show="!login">
          Sign up:
      </header>
      <section class="modal-body" v-show="login">
          <form  v-on:submit.prevent="onSubmit" v-on:submit='logMeIn'>
              <label>Username:</label>
              <input type='text' v-bind:value="user" v-on:input="user = $event.target.value" />
              <br />
              <label>Password:</label>
              <input type='password' v-bind:value="pass" v-on:input="pass = $event.target.value"/>
              <br />
              <button type="submit" @click="logMeIn">Login</button>
          </form>
          <span>{{warning}}</span>
          <div v-show='login'>
              Not a member?<a href="url" @click.prevent='login=!login'> Sign up here!</a>
              </div>
        </section>
        <section class="modal-body" v-show="!login">
          <form  v-on:submit.prevent="onSubmit" v-on:submit='signMeUp'>
              <label>Username:</label>
              <input type='text' v-bind:value="user" v-on:input="user = $event.target.value" />
              <br />
              <label>Password:</label>
              <input type='password' v-bind:value="pass" v-on:input="pass = $event.target.value"/>
              <br />
              <button type="submit" @click="logMeIn">Login</button>
          </form>
          <span>{{warning}}</span>
          <div v-show='!login'>
              Already a member?<a href="url" @click.prevent='login=!login'> Login here!</a>
              </div>
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
  name: 'loginModal',
  data() {
    return {
      login: true,
      user: '',
      pass: '',
      warning: '',
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    logMeIn() {
      const payload = JSON.parse(`{"username": "${this.user}", "password": "${this.pass}"}`);
      const path = 'http://localhost:5000/login';
      this.warning = '';
      axios.post(path, payload).then((res) => {
        if (res.data.success === true) {
          localStorage.user = payload.username;
          this.close();
        }
      }).catch((error) => {
        if (error.response) {
          this.warning = 'Invalid username or password!';
        }
      });
    },
    signMeUp() {
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
