const SingUp = () => {
  function applyFieldMask() {
    $('#id_username').mask('A', {
      translation: {
        'A': {
          pattern: /[a-zA-Z0-9@.+_-]/,
          recursive: true,
        },
      }
    });

    $('#id_email').mask('A', {
      translation: {
        'A': { pattern: /[\w@\-.+]/, recursive: true }
      }
    });

    $('#id_phone').mask('(000) 00000-0000');
  }

  function handleFormValidation() {
    $('#singup_form').validate({
      errorElement: 'div',
      errorClass: 'invalid-feedback',
      highlight: function(element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      },
      rules: {
        username: {
          required: true,
          minlength: 3,
          maxlength: 150
        },
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
        email: {
          required: true,
          minlength: 3,
          maxlength: 254,
        },
        phone: {
          required: true,
        },
        password1: {
          required: true,
          minlength: 8,
        },
        password2: {
          required: true,
          equalTo: '#id_password1',
        },
      },
      messages: {
        username: {
          required: 'O nome de usuário deve ser inserido.',
          minlength: 'O nome de usuário deve ter pelo menos 3 caracteres.',
          maxlength: 'O nome de usuário não pode ter mais de 150 caracteres.'
        },
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
        email: {
          required: 'O email deve ser inserido.',
          minlength: 'O email deve ter pelo menos 3 caracteres.',
          maxlength: 'O email não pode ter mais de 254 caracteres.',
          email: 'Por favor, insira um endereço de e-mail válido.'
        },
        phone: {
          required: 'O telefone deve ser inserido.',
        },
        password1: {
          required: 'A senha deve ser inserida.',
          minlength: 'A senha deve ter pelo menos 8 caracteres.',
        },
        password2: {
          required: 'A confirmação de senha deve ser inserida.',
          equalTo: 'As senhas não coincidem. Por favor, verifique.',
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

    $('#id_username').keyup(function(e) {
      $(this).valid();
    });

    $('#id_first_name').keyup(function(e) {
      $(this).valid();
    });

    $('#id_last_name').keyup(function(e) {
      $(this).valid();
    });

    $('#id_email').keyup(function(e) {
      $(this).valid();
    });

    $('#id_phone').keyup(function(e) {
      $(this).valid();
    });

    $('#id_password1').keyup(function(e) {
      $(this).valid();
    });

    $('#id_password2').keyup(function(e) {
      $(this).valid();
    });
  }

  function addBootstrapMaxLength() {
    $('#id_username').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });

    $('#id_first_name').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });

    $('#id_last_name').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });

    $('#id_email').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });

    $('#id_rgm').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });
  }

  function handleSubmit() {
    $('#singup_form').submit(function() {
      $('#id_phone').unmask();
    });
  }

  applyFieldMask();
  addBootstrapMaxLength();
  handleSubmit();
  handleFormValidation();
}

KTUtil.onDOMContentLoaded(function() {
  SingUp();
});
