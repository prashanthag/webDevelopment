//window.onload = function (){
  var app = new Vue({
    el: '#app',
    data: {
      message: 'Hello Vue!',
      mouseMsg: 'Date, time: ' + new Date().toLocaleString(),
      //mouseMsg: 'You loaded this page on ' + new Date().toLocaleString(),
      look: 'font-size:20px;border:3px solid green;color:red',
      bool: true,
      array: [34,56,23,67,89],
      todo: [
              {text:"Hello 1"},
              {text:"Hello 2"},
              {text:"Hello 3"},
              {text:"Hello 4"},
              {text:"Hello 5"},
              {text:"Hello 6"},
      ],
      groceryList: [
        {id:1,text:'Vegetables'},
        {id:2,text:'Cheese'},
        {id:3,text:'whatever human suppose to help'},
      ],
    },
    methods: {
      reverse: function(){
        //this.message = this.message+' concateed message'
        this.message = this.message.split('').reverse().join('')
      },

    },
  });
Vue.component('vdo', {
  props: ['tod'],
  template: '<li> {{tod.text}}</li>',
})

  //app.message = "Assign here different message"

//}
