// custom javascript

$(document).ready(() => {
  console.log('Sanity Check!');
});

$('form').submit(function(event) {
  var formdata = $(this).serializeObject();
  console.log(formdata);
  event.preventDefault();
  
  $("#loading").toggleClass("invisible");
  $("#submitBtn").toggleClass("invisible");

  $.ajax(
    {
      url: '/enqueue',
      data: formdata,
      type: 'POST',
      dataType: 'JSON'
    }
  )
  .done((res) => {
    getStatus(res.data.task_id)
  })
  .fail((err) => {
    console.log(err)
  })
})

function getStatus(taskID) {
  $.ajax({
    url: `/tasks/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const taskStatus = res.data.task_status;

    if (taskStatus === 'finished' || taskStatus === 'failed') {
      window.location.assign(`/results/${taskID}`);
      $("#loading").toggleClass("invisible");
      $("#submitBtn").toggleClass("invisible");
      return false;
    }
    setTimeout(function() {
      getStatus(res.data.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  })
}
