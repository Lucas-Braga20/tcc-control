const TimetableEditor = () => {
  let stageEditor = null;


  function addFormValidator() {
    $('#tcc_editor_timetables').validate({
      errorElement: 'div',
      errorClass: 'invalid-feedback',
      highlight: function(element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      },
      rules: {
        description: {
          required: true,
          minlength: 3,
          maxlength: 255
        },
        mentee_field: {
          required: true,
        },
        supervisor_field: {
          required: true,
        }
      },
      messages: {
        description: {
          required: 'A descrição deve ser inserida.',
          minlength: 'A descrição deve ter pelo menos 3 caracteres.',
          maxlength: 'A descrição não pode ter mais de 255 caracteres.'
        },
        mentee_field: {
          required: 'Os orientandos devem ser selecionados.',
        },
        supervisor_field: {
          required: 'Os orientadores devem ser selecionados.',
        },
      },
      errorPlacement(error, element) {
        element.parent().append(error);
      },
    });

    $('#description').keyup(function(e) {
      $(this).valid();
    });
  }

  function addBootstrapMaxLength() {
    $('#description').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });
  }

  function handleSelect2Elements() {
    $('[data-control="select2"]').on('select2:select', function(e) {
      $(this).valid();
    });

    $('[data-control="select2"]').on('select2:unselect', function(e) {
      $(this).valid();
    });
  }


  stageEditor = new StageEditor();
  addFormValidator();
  addBootstrapMaxLength();
  handleSelect2Elements();
}

KTUtil.onDOMContentLoaded(function() {
  TimetableEditor();
});
