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

  function handleSubmit() {
    $('#tcc_profile_form').submit(function() {
      $('#id_phone').unmask();
    });
  }

  applyFieldMask();
  addBootstrapMaxLength();
  handleSubmit();
}

KTUtil.onDOMContentLoaded(function() {
  Profile();
});
