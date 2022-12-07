const list_el =document.querySelector(".con")

function addWorkSettings(){
  const form_el = document.createElement("form")
  form_el.classList.add("work__settings__task__adding")
  const task_input_filr_el = document.createElement("input")
  task_input_filr_el.classList.add("work__settings__file__adding")
  form_el.method ="post"
  task_input_filr_el.type="file"
  task_input_filr_el.accept="image/*"
  const task_input_answer_el=document.createElement("input")
  task_input_answer_el.classList.add("work__settings__answer__adding")
  task_input_answer_el.type = ("text")
  task_input_answer_el.placeholder =("Предполагаемый ответ")
  form_el.appendChild(task_input_filr_el)
  form_el.appendChild(task_input_answer_el)
  list_el.appendChild(form_el)
}
function delWorkSettings(){
  list_el.removeChild(list_el.lastChild)
}
const form =document.querySelector(".add__work")
form.addEventListener('submit', function (event) {
  event.preventDefault()
  addWorkSettings()
})
const form1 =document.querySelector(".delete__work")
form1.addEventListener('submit', function (event) {
  event.preventDefault()
  delWorkSettings()
})