function formToggle(id){
    const form = document.querySelector('#form' + id);
    const button = document.querySelector('#mybtn3');
    


    if(form.style.display === 'none'){
        form.style.display = 'block'
        button.style.display = 'none'
        
    }
    else{
        form.style.display = 'none'
        button.style.display = 'block'
       
    }

}


  const commentsForm = document.getElementById('comment_form');
  const csrf = document.querySelector('#csrf input')
  const blog = document.getElementById('id_blog')
  const text = document.querySelector('#comment_form #id_text')
  const author = document.querySelector('#comment_form #id_author')
  const submitBtn = document.querySelector('#comment_form button')
  const commentSec = document.getElementById('commentsSec');
  const formInput = document.querySelector('#comment_form #id_text')
  console.log(commentSec)
  console.log(formInput)

  const submitForm = () => {
    $.ajax({
      type: 'POST',
      url: '/blog/save_comment/',
      data: {
          'blog': blog.value,
          'text': text.value,
          'author': author.value,
          'csrfmiddlewaretoken': csrf.value
      },
      headers: {
      'X-Requested-With': 'XMLHttpRequest'
      },
      success: (res) => {
        console.log(res)
        const comments = res.fcomments
        let comSecInnerHTML = ''
        
        const counter = (parseInt(document.querySelector('#commentsCount').innerText) + 1) || 0;
        comments.forEach((comment, index) => {
          comSecInnerHTML += `
          <h4 class="mb-0"><i class="bi bi-person-circle text-secondary mb-0 me-2"></i>${ comment.author }</h4>
          <p class="ms-4 mt-0 mb-0 rounded border-top border-left border-right p-3 pb-0"  style="color: rgb(160, 160, 160);"><small>${ comment.date_published } ago.</small></p>
          <p class="ms-4 p-3 pt-0 mt-0 rounded border-bottom border-left border-right">${comment.text}</p>
          <button type="button" class="ms-4 btn btn-small btn-outline-secondary" id="mybtn3" onclick="formToggle(${index + 1})" style="display: block;">reply</button>
          <hr>
          <div id="form${index + 1}" class="commentreplyform" style="display: none;">
          <form id="commentReply" faction="/blog/save_commentreply/${comment.id}/" method="POST" style="padding-top: 0;">
          <button type="button" class="btn btn-small btn-secondary-outline" id="mybtn4" onclick="formToggle(${index + 1 })" style="display: block;">x</button>
              <span id="commentReplyCsrf"><input type="hidden" name="csrfmiddlewaretoken" value="${ comment.token }"></span>
              <p>Reply to ${ comment.author }</p>
              <span id="authorId" class="d-none"><input type="hidden" id="id_author" name="author" value="${res.userId}"></span>
              <p>Text</p>
              <textarea name="text" cols="40" rows="10" class="form-control" style="width: 40%; height: 60px" required="" id="id_text"></textarea>
              <button onclick="repo(event)" id="commentreplyBtn" counter=(${index}) class="commentreplyBtn  btn btn-outline-primary">Post comment</button>
          </form>
          </div>
          
          `
            if(comment.commentReplies.length > 0){
              let repSecInnerHTML = '<div class="border-left ps-2"  id="commentreplies">'
              for(comment of comment.commentReplies){
                repSecInnerHTML += `
              
                <h6 class="mb-0"><i class="bi bi-person-circle text-secondary mb-0 me-2"></i>${ comment.author}</h6>    
                <p  class="ms-4 mt-0 mb-0 rounded border-top border-left border-right p-3 pb-0" style="color: rgb(160, 160, 160);"><small>${comment.publishedDate} ago</small></p>
               <p class="ms-4 p-3 pt-0 mt-0 rounded border-bottom border-left border-right">${ comment.text}</p>
               <hr>

              `
             
              }
              repSecInnerHTML += '</div>'
              comSecInnerHTML += repSecInnerHTML

            
            }
        })
        commentSec.innerHTML = comSecInnerHTML

        formInput.value = ''
        formInput.blur()

       
      },
      error: (err) => {
        console.log(err)
      }

    })
  }

  submitBtn.addEventListener('click', (e) => {
        e.preventDefault();
        submitForm()
  })


//n cost commentReplyForm = document.getElementById('#commentReply');
const submitReplyBtn = document.querySelectorAll('.commentreplyBtn');
const commentreplyBtn = document.querySelectorAll('.commentreplyBtn');
const replyTxt = document.querySelector('commentReply #id_text');
const commentReplyCsrf = document.querySelector('#commentReplyCsrf input').value;
submitReplyBtn.forEach((button) => {
console.log(button)
})
console.log()


const submitCommmentReply = (text, url, author, commentReplies, Xbtn) => {
$.ajax({
type: 'POST',
url: url,
headers: {
  'X-Requested-With': 'XMLHttpRequest'
},
data:{
 'text': text.value,
  'author': author,
  'csrfmiddlewaretoken': commentReplyCsrf
},
success: (res) => {
  console.log(res)
  replies = res.data.commentReplies
  let innerHTML = ''
  for (let reply of replies){
    innerHTML += `
  <h6 class="mb-0"><i class="bi bi-person-circle text-secondary mb-0 me-2"></i>${ reply.author}</h6>    
  <p  class="ms-4 mt-0 mb-0 rounded border-top border-left border-right p-3 pb-0" style="color: rgb(160, 160, 160);"><small>${reply.date_published}ago.</small></p>
  <p class="ms-4 p-3 pt-0 mt-0 rounded border-bottom border-left border-right">${ reply.text}</p>
  <hr>
  `
  }
  commentReplies.innerHTML = innerHTML
  text.value = ''
  Xbtn
  console.log(Xbtn)
  
  
},
error: (err) => {
  console.log(err)
}
})
}

submitReplyBtn.forEach((btn) => {
btn.addEventListener('click', (e) => {
e.preventDefault()
const url = btn.parentElement.getAttribute('faction');
const text = btn.parentElement.children[4];
const author = btn.parentElement.children[3].firstChild.nextElementSibling.value || document.getElementById('authorId').firstChild.value;
const commentReplies = btn.parentElement.parentElement.nextElementSibling;
const Xbtn = btn.parentElement.firstElementChild.getAttribute('onclick')

console.log(commentReplies)
console.log(author)

submitCommmentReply(text, url, author, commentReplies, Xbtn)
} )
})


function repo (event){
event.preventDefault()
//n cost commentReplyForm = document.getElementById('#commentReply');
const submitReplyBtn = document.querySelectorAll('.commentreplyBtn');
const commentreplyBtn = document.querySelectorAll('.commentreplyBtn');
const replyTxt = document.querySelector('commentReply #id_text');
const commentReplyCsrf = document.querySelector('#commentReplyCsrf input').value;
submitReplyBtn.forEach((button) => {
console.log(button)
})
console.log()


const submitCommmentReply = (text, url, author, commentReplies, Xbtn) => {
$.ajax({
type: 'POST',
url: url,
headers: {
  'X-Requested-With': 'XMLHttpRequest'
},
data:{
 'text': text.value,
  'author': author,
  'csrfmiddlewaretoken': commentReplyCsrf
},
success: (res) => {
  console.log(res)
  replies = res.data.commentReplies
  let innerHTML = ''
  for (let reply of replies){
    innerHTML += `
    
    <h6 class="mb-0"><i class="bi bi-person-circle text-secondary mb-0 me-2"></i>${reply.author}</h6>    
    <p  class="ms-4 mt-0" style="color: rgb(160, 160, 160);"><small>${reply.date_published} ago.</small></p>
    <p>${reply.text}</p>
    <hr>
    
  `
  }
  commentReplies.innerHTML = innerHTML
  text.value = ''
  Xbtn
  console.log(Xbtn)
  
  
},
error: (err) => {
  console.log(err)
}
})
}

submitReplyBtn.forEach((btn) => {
if(btn.getAttribute('counter') === event.target.getAttribute('counter') ){
const url = btn.parentElement.getAttribute('faction');
const text = btn.parentElement.children[5];
const author = document.getElementById('authorId').firstChild.value;
const commentReplies = btn.parentElement.parentElement.nextElementSibling;
const Xbtn = btn.parentElement.firstElementChild.getAttribute('onclick')
const  data = {
 'text': text.value,
  'author': author,
  'csrfmiddlewaretoken': commentReplyCsrf
}
console.log(commentReplies)
console.log(author)
console.log(data)
console.log(text)
console.log(btn.getAttribute('counter'))
console.log(event.target.getAttribute('counter'))


submitCommmentReply(text, url, author, commentReplies, Xbtn)
}

} )
}

submitReplyBtn.forEach((btn) => {
btn.parentElement.children[4].addEventListener('keyup', (e) => {
    console.log(btn.parentElement.children[4].value)
})

})