const ActivityConfigurationEditor = () => {
  let fieldsEditor = null;


  function addFormValidator() {
    $('#tcc_editor_activity_configurations').validate({
      errorElement: 'div',
      errorClass: 'invalid-feedback',
      highlight: function(element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      },
      rules: {
        name: {
          required: true,
          minlength: 3,
          maxlength: 255
        },
      },
      messages: {
        name: {
          required: 'A descrição deve ser inserida.',
          minlength: 'A descrição deve ter pelo menos 3 caracteres.',
          maxlength: 'A descrição não pode ter mais de 255 caracteres.'
        },
      },
    });

    $('#tcc_editor_activity_configurations').submit(function(event) {
      const value = $('[name="fields"]').val();

      if (value == null || value == '' || value == 'null') {
        $('[name="fields"]').addClass('is-invalid');
        $('[name="fields"]').after(`
          <div class="invalid-feedback">
            Os campos da atividade devem ser inseridos.
          </div>
        `);
      }
      else {
        $('[name="fields"]').removeClass('is-invalid');
        $('[name="fields"]').parent().find('.invalid-feedback').remove();
      }
    });
  }

  function addBootstrapMaxLength() {
    $('#id_name').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });
  }


  fieldsEditor = new ActivityFieldsEditor()
  addFormValidator();
  addBootstrapMaxLength();
}

KTUtil.onDOMContentLoaded(function() {
  ActivityConfigurationEditor();
});
