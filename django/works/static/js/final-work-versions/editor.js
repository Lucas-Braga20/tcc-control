const FinalWorkVersionEditor = () => {
  let richTextEditors = tinymce.init({
    selector: '.tcc_rich_text',
    height: 400,
  });

  let contentInputElement = $('#id_content');
  let submitButtonElement = $('#tcc_submit_button');


  function setContentValues() {
    const json = JSON.parse(contentInputElement.val());

    json.fields.forEach(field => {
      const element = $(`[name="content__${ field.key }"]`);

      if (element.data('type') === 'text' || element.data('type') === 'number') {
        $(`[name="content__${ field.key }"]`).val(field.value);
      } else if (element.data('type') === 'rich') {
        tinymce.get(element.get(0).id).setContent(field.value);
      }
    });
  }

  function handleSubmitButtonEvent() {
    $(submitButtonElement).click(function (e) {
      let response = {
        fields: [],
      };

      $('.tcc_content_field').each(function () {
        if ($(this).data('type') === 'text' || $(this).data('type') === 'number') {
          response.fields.push({
            key: $(this).data('key'),
            value: $(this).val(),
          });
        } else if ($(this).data('type') === 'rich') {
          response.fields.push({
            key: $(this).data('key'),
            value: tinymce.get($(this).get(0).id).getContent(),
          });
        }
      });

      $(contentInputElement).val(JSON.stringify(response));

      $('#tcc_version_form').submit();
    });
  }


  setContentValues();
  handleSubmitButtonEvent();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkVersionEditor();
});
