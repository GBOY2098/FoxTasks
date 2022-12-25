const list_el =document.querySelector(".con")
var i=1;
function addWorkSettings(x){
  const form_el = document.createElement("div")
  form_el.classList.add("work__settings__task__adding")
  const task_input_file_el = document.createElement("input")
  task_input_file_el.classList.add("work__settings__file__adding")
  const task_input_image_el = document.createElement("input")
  task_input_image_el.classList.add("work__settings__file__adding")
  form_el.method ="post"
  task_input_file_el.type="file"
  task_input_image_el.type="file"
  task_input_image_el.accept="image/*"
  const task_input_answer_el=document.createElement("input")
  task_input_answer_el.classList.add("work__settings__answer__adding")
  task_input_answer_el.type = ("text")
  task_input_answer_el.placeholder =("Предполагаемый ответ")
  task_input_answer_el.name= ("answer"+x.toString(10))
  task_input_file_el.name= ("file"+x.toString(10))
  task_input_image_el.name= ("image"+x.toString(10))
  form_el.appendChild(task_input_image_el)
  form_el.appendChild(task_input_file_el)
  form_el.appendChild(task_input_answer_el)
  list_el.appendChild(form_el)
}
function delWorkSettings(x){
  list_el.removeChild(list_el.lastChild)
}
const form =document.querySelector(".add__work")
form.addEventListener('submit', function (event) {
  event.preventDefault()
  addWorkSettings(i)
  i++
})
const form1 =document.querySelector(".delete__work")
form1.addEventListener('submit', function (event) {
  event.preventDefault()
  delWorkSettings(i)
  i--
})