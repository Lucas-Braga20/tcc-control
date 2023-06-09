const FormularyTestEditor = () => {
  // Variables
  let formElement;

  let contentTextAreaElement;
  let contentLoadingElement;

  let contentCkEditor;


  // Methods
  function getElements() {
    formElement = document.getElementById('kt_form_activity');
    contentTextAreaElement = document.getElementById('kt_content_ck_editor');
    contentLoadingElement = document.getElementById('kt_content_ck_editor_loading');
  }

  function initContentEditor() {
    ClassicEditor
      .create(contentTextAreaElement)
      .then(editor => {
        contentCkEditor = editor;

        contentLoadingElement.classList.add('d-none');
        contentTextAreaElement.classList.remove('d-none');
      })
      .catch(error => {
        console.error(error);
      });
  }


  // Constructor
  getElements();
  initContentEditor();
}

KTUtil.onDOMContentLoaded(function() {
  FormularyTestEditor();
});
