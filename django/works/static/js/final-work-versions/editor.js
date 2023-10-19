const FinalWorkVersionEditor = () => {
  tinymce.init({
    selector: '.tcc_rich_text',
    height: 400,
    images_upload_url: '/version-content-images/',
    images_upload_base_path: '/api',
    plugins: [
      'table paste image media imagetools lists',
    ],
    toolbar: 'undo redo | styleselect | bold italic underline | table | image | bullist',
    formats: {
      titulo1: { block: 'h1' },
      titulo2: { block: 'h2' },
      titulo3: { block: 'h3' },
      citacao: { block: 'blockquote' },
      referencia: { block: 'div' },
      paragrafo: { block: 'p' },
    },
    style_formats: [
      { title: 'Paragrafo', format: 'paragrafo' },
      { title: 'Titulo 1', format: 'titulo1' },
      { title: 'Titulo 2', format: 'titulo2' },
      { title: 'Titulo 3', format: 'titulo3' },
      { title: 'Citação', format: 'citacao' },
      { title: 'Referência', format: 'referencia' },
    ],
    images_upload_handler(blobInfo, success, failure, progress) {
      let xhr, formData;

      xhr = new XMLHttpRequest();
      xhr.withCredentials = false;
      xhr.open('POST', '/api/version-content-images/');
      xhr.setRequestHeader('X-CSRFToken', $('[name="csrfmiddlewaretoken"]').val());

      xhr.upload.onprogress = function (e) {
        progress(e.loaded / e.total * 100);
      };

      xhr.onload = function() {
        var json;
    
        if (xhr.status === 403) {
          failure('HTTP Error: ' + xhr.status, { remove: true });
          return;
        }
    
        if (xhr.status < 200 || xhr.status >= 300) {
          failure('HTTP Error: ' + xhr.status);
          return;
        }
    
        json = JSON.parse(xhr.responseText);
        json['location'] = json['image']
    
        if (!json || typeof json.location != 'string') {
          failure('Invalid JSON: ' + xhr.responseText);
          return;
        }
    
        success(json.location);
      };

      xhr.onerror = function () {
        failure('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
      };
    
      formData = new FormData();
      formData.append('image', blobInfo.blob(), blobInfo.filename());
      formData.append('version', $('#tcc_version_form').data('version'));

      xhr.send(formData);
    },
    paste_preprocess: function (plugin, args) {
      args.content = args.content.replace(/<[^>]*>/g, "");
    },
  });

  let contentInputElement = $('#id_content');
  let submitButtonElement = $('#tcc_submit_button');


  function configEditor() {
    $('.tcc_rich_text[disabled=true]').each(function() {
      tinymce.get($(this).get(0).id).setMode('readonly');
    });
  }


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
  configEditor();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkVersionEditor();
});
