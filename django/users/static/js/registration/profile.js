const Profile = () => {
  function applyFieldMask() {
    $('#id_phone').mask('(000) 00000-0000');
  }

  function addBootstrapMaxLength() {
    $('#id_first_name').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });

    $('#id_last_name').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });

    $('#id_rgm').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });

    $('#id_university_course').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });
  }

  function handleFormValidation() {
    $('#tcc_profile_form').validate({
      errorElement: 'div',
      errorClass: 'invalid-feedback',
      highlight: function(element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      },
      rules: {
        first_name: {
          required: true,
          minlength: 3,
          maxlength: 30,
        },
        last_name: {
          required: true,
          minlength: 3,
          maxlength: 30,
        },
        phone: {
          required: true,
        },
      },
      messages: {
        first_name: {
          required: 'O primeiro nome deve ser inserido.',
          minlength: 'O primeiro nome deve ter pelo menos 3 caracteres.',
          maxlength: 'O primeiro nome não pode ter mais de 30 caracteres.'
        },
        last_name: {
          required: 'O segundo nome deve ser inserido.',
          minlength: 'O segundo nome deve ter pelo menos 3 caracteres.',
          maxlength: 'O segundo nome não pode ter mais de 30 caracteres.'
        },
        phone: {
          required: 'O telefone deve ser inserido.',
        },
      },
      highlight: function(element) {
        $(element).siblings('.tcc_help_text').addClass('d-none');
        $(element).siblings('ul').addClass('d-none');
      },
      unhighlight: function(element) {
        $(element).siblings('.tcc_help_text').removeClass('d-none');
        $(element).siblings('ul').removeClass('d-none');
      }
    });

    $('#id_first_name').keyup(function(e) {
      $(this).valid();
    });

    $('#id_last_name').keyup(function(e) {
      $(this).valid();
    });

    $('#id_phone').keyup(function(e) {
      $(this).valid();
    });
  }

  function handleSubmit() {
    $('#tcc_profile_form').submit(function() {
      $('#id_phone').unmask();
    });
  }

  applyFieldMask();
  addBootstrapMaxLength();
  handleFormValidation();
  handleSubmit();
}

KTUtil.onDOMContentLoaded(function() {
  Profile();
});
