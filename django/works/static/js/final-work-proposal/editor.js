const FinalWorkEditor = () => {
  let menteesSelectElement = null;


  function getElements() {
    menteesSelectElement = $('[name="mentees"]');
  }

  function handleMenteesSelectElement() {
    $(menteesSelectElement).on('select2:unselecting', e => {
      const currentUser = $('[name="current-user"]').val();
    
      const userWillBeRemoved = e.params.args.data.id;
    
      if (currentUser === userWillBeRemoved) {
        e.preventDefault();
      }
    });
    
    $(menteesSelectElement).on('select2:selecting', e => {
      const selectedItems = $('[name="mentees"]').select2('val');
    
      if (selectedItems.length > 1) {
        e.preventDefault();
      }
    });
  }

  function addFormValidator() {
    $('#work_proposal_editor').validate({
      errorElement: 'div',
      errorClass: 'invalid-feedback',
      highlight: function(element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      },
      rules: {
        title: {
          required: true,
          minlength: 3,
          maxlength: 128,
        },
        description: {
          required: true,
          minlength: 3,
          maxlength: 255
        },
        supervisor: {
          required: true,
        },
      },
      messages: {
        title: {
          required: 'O título deve ser inserido.',
          minlength: 'O título deve ter pelo menos 3 caracteres.',
          maxlength: 'O título não pode ter mais de 128 caracteres.'
        },
        description: {
          required: 'A descrição deve ser inserida.',
          minlength: 'A descrição deve ter pelo menos 3 caracteres.',
          maxlength: 'A descrição não pode ter mais de 255 caracteres.'
        },
        supervisor: {
          required: 'O orientador deve ser selecionado.',
        },
      },
      errorPlacement(error, element) {
        element.parent().append(error);
      },
    });

    $('#id_title').keyup(function(e) {
      $(this).valid();
    });

    $('#id_description').keyup(function(e) {
      $(this).valid();
    });

    $('[data-control="select2"]').on('select2:select', function(e) {
      $(this).valid();
    });

    $('[data-control="select2"]').on('select2:unselect', function(e) {
      $(this).valid();
    });
  }

  function addBootstrapMaxLength() {
    $('#id_description').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });

    $('#id_title').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });
  }


  getElements();
  handleMenteesSelectElement();

  addFormValidator();
  addBootstrapMaxLength();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkEditor();
});
