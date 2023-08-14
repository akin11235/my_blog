function likeHandler(event) {
  event.preventDefault();

  const element = event.currentTarget;

  const commentId = element.dataset.commentId;

  const action = element.classList.contains("like") ? "like" : "dislike";

  fetch(`/comments/${commentId}/${action}/`, {
    method: "POST",
    headers: { "X-CSRFToken": csrftoken },
  })
    .then((response) => response.json())
    .then((data) => {
      const likesCountElement = document.querySelector(
        `#likes-count-${commentId}`
      );
      const dislikesCountElement = document.querySelector(
        `#dislikes-count-${commentId}`
      );
      likesCountElement.textContent = data.likes;
      dislikesCountElement.textContent = data.dislikes;
    });
}
document.querySelectorAll(".like, .dislike").forEach((link) => {
  link.addEventListener("click", likeHandler);
});


//const pre = document.querySelector('pre');
//
//function likeHandler(event) {
//	event.preventDefault();
//
//  // Get the element that was clicked on. It's the event
//  // currentTarget property.
//  const element = event.currentTarget;
//  // This is an <a> tag and has a readable href property
//
//  // Print out the result
//  pre.textContent = 'URL:  ' + element.href + '\n';
//
//}
//
//// Select multiple classes: both like & dislike buttons
//document.querySelectorAll('.like, .dislike')
//	.forEach(function (link) {
//		link.addEventListener('click', likeHandler);
//	});

//function likeHandler(event) { event.preventDefault();
//
//const element = event.currentTarget;
//
//const commentId = element.dataset.commentId;
//
//const action = element.classList.contains('like') ? 'like' : 'dislike';

//fetch(`/comments/${commentId}/${action}/`, { method: 'POST', headers: { 'X-CSRFToken': csrftoken }, }) .then(response => response.json()) .then(data => { const likesCountElement = document.querySelector(`#likes-count-${commentId}`); const dislikesCountElement = document.querySelector(`#dislikes-count-${commentId}`); likesCountElement.textContent = data.likes; dislikesCountElement.textContent = data.dislikes; }); } document.querySelectorAll('.like, .dislike') .forEach(link => { link.addEventListener('click', likeHandler); });