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
  }

  function handleSubmit() {
    $('#singup_form').submit(function() {
      $('#id_phone').unmask();
    });
  }

  applyFieldMask();
  addBootstrapMaxLength();
  handleSubmit();
}

KTUtil.onDOMContentLoaded(function() {
  SingUp();
});
