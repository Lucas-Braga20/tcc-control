KTUtil.onDOMContentLoaded(function() {
  ClassicEditor
    .create(document.querySelector('#kt_ckeditor_content'))
    .catch(error => {
      console.error(error);
    });
});
