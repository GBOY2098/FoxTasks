var src1 = "Tasks/Picsart_22-11-10_19-58-45-176.jpg"
var src2 = "Tasks/Picsart_22-11-10_19-59-41-244.jpg"
var src3 = "Tasks/Picsart_22-11-10_20-00-36-549.jpg"
var src4 = "Tasks/Picsart_22-11-10_20-01-03-923.jpg"
// const form =document.querySelector(".task__form")
// const answer = document.querySelector(".task__answer")
const list_el =document.querySelector(".tasks")
function addTask(src,task_number){
  const task_el = document.createElement("article")
  task_el.classList.add("task")
  const task_form_el = document.createElement("form")
  task_form_el.classList.add("task__form"+String(task_number))
  task_form_el.method ="get"
  const task_img_el = document.createElement("img")
  task_img_el.classList.add("task__photo")
  task_img_el.src = (src)
  const task_answer_el=document.createElement("input")
  task_answer_el.classList.add("task__answer"+String(task_number))
  task_answer_el.type = ("text")
  task_answer_el.placeholder =("Введите ответ")
  const task_button_el= document.createElement("input")
  task_button_el.classList.add("task__button")
  task_button_el.type = ("submit")
  task_form_el.innerHTML="Ответ:"
  task_el.appendChild(task_img_el)
  task_el.appendChild(task_form_el)
  task_form_el.appendChild(task_answer_el)
  task_form_el.appendChild(task_button_el)
  list_el.appendChild(task_el)
}
for(var i=1; i<5;i++){
  addTask(eval("src"+String(i)),i)
}




