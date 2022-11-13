let src = ["Tasks/Picsart_22-11-10_19-58-45-176.jpg","Tasks/Picsart_22-11-10_19-59-41-244.jpg","Tasks/Picsart_22-11-10_20-00-36-549.jpg","Tasks/Picsart_22-11-10_20-01-03-923.jpg"]
var correct_answer = ["10",'11','12','13']
const list_el =document.querySelector(".tasks")
function addTask(src,task_number){
  const task_el = document.createElement("article")
  task_el.classList.add("task"+String(task_number),"task")
  const task_form_el = document.createElement("form")
  task_form_el.classList.add("task__form"+String(task_number),"form")
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
for(var i=1; i<5 ;i++){ 
  addTask(src[i-1],i)
}

// for(var i=1; i<5 ;i++){ 
  const form1 =document.querySelector(".task__form"+String(1))
  form1.addEventListener('submit', function (event) {
    event.preventDefault()
    const answer = document.querySelector(".task__answer"+String(1))
    const task_el = document.querySelector(".task"+String(1))
    if (answer.value==correct_answer[0]){
      const answer_correction_el=document.createElement("div")
      answer_correction_el.classList.add("true","container")
      answer_correction_el.innerHTML = "Верно"
      task_el.appendChild(answer_correction_el)
    }else{
      const answer_correction_el=document.createElement("div")
      answer_correction_el.classList.add("false","container")
      answer_correction_el.innerHTML="Неверно" 
      task_el.appendChild(answer_correction_el)
    }
  })
// }
const form2 =document.querySelector(".task__form"+String(2))
console.log(form2)
form2.addEventListener('submit', function (event) {
  event.preventDefault()
  const answer = document.querySelector(".task__answer"+String(2))
  const task_el = document.querySelector(".task"+String(2))
  if (answer.value==correct_answer[1]){
    const answer_correction_el=document.createElement("div")
    answer_correction_el.classList.add("true","container")
    answer_correction_el.innerHTML = "Верно"
    task_el.appendChild(answer_correction_el)
  }else{
    const answer_correction_el=document.createElement("div")
    answer_correction_el.classList.add("false","container")
    answer_correction_el.innerHTML="Неверно" 
    task_el.appendChild(answer_correction_el)
  }
})
