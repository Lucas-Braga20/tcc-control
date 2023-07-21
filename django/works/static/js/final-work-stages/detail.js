const FinalWorkStageDetail = () => {
  let workStageId = $('#kt_content_container').data('work-stage');

  let commentsContainer = null;
  let addCommentButton = null;
  let commentDescriptionTextarea = null;

  let meetingsContainer = null;

  let modal = {
    element: null,
    object: null,
    cancelButton: null,
    confirmButton: null,
    requestButton: null,
    closeButton: null,
  };

  const API = {
    comments: {
      list() {
        return fetch(`/api/comments/?no_page=true&work_stage=${workStageId}`, {
          method: 'get',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      add(description) {
        return fetch(`/api/comments/`, {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            work_stage: workStageId,
            description: description,
          }),
        });
      },
    },
    meetings: {
      list() {
        return fetch(`/api/meetings/?no_page=true&work_stage=${workStageId}`, {
          method: 'get',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      add(description, meetingDate) {
        return fetch(`/api/meetings/`, {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            work_stage: workStageId,
            meeting_date: meetingDate,
            description,
          }),
        });
      },
    },
  };


  function getElements() {
    commentsContainer = $('#tcc_comments_container');
    addCommentButton = $('#tcc_add_comment');
    commentDescriptionTextarea = $('#tcc_comment_textarea');
    meetingsContainer = $('#tcc_request_meetings_container');
    modal.element = $('#tcc_request_meeting_modal');
    modal.object = new bootstrap.Modal(modal.element);
    modal.requestButton = $('#tcc_request_meeting_request_button');
    modal.cancelButton = $('#tcc_request_meeting_modal_cancel');
    modal.confirmButton = $('#tcc_request_meeting_modal_confirm');
    modal.closeButton = $('#tcc_request_meeting_modal_close');
  }


  // Comments
  function getAllComments() {
    API.comments.list()
      .then(response => response.json())
      .then(response => {
        let comments = '';

        if (response.length == 0) {
          $(commentsContainer).html(`
            <div class="p-4 border rounded">
              <div class="mt-2">
                <p class="mb-0">
                  Sem comentários
                </p>
              </div>
            </div>
          `);

          return;
        }

        response.forEach(comment => {
          comments += `
            <div class="p-4 border rounded mt-2">
              <div class="d-flex justify-content-between text-gray-500">
                <h5 class="mb-0">
                  ${comment.author_detail.full_name}
                </h5>
                <span>
                  ${moment(comment.created_at).format('DD/MM/YYYY HH:mm')}
                </span>
              </div>
              <div class="mt-2">
                <p class="mb-0">
                  ${comment.description}
                </p>
              </div>
            </div>
          `;
        });
        $(commentsContainer).html(comments);
      })
      .then(() => {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl);
        });
      });
  }

  function initAddCommentEvent() {
    $(addCommentButton).click(e => {
      $(commentDescriptionTextarea).attr('disabled', true);
      $(addCommentButton).attr('disabled', true);

      $(addCommentButton).html(`
        <div class="spinner-border spinner-border-sm text-white me-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        Comentar
      `);

      API.comments.add($(commentDescriptionTextarea).val())
        .then(response => {
          if (response.ok === false) {
            throw new Error(response.statusText);
          }

          return response.json();
        })
        .then(response => {
          getAllComments();

          $(commentDescriptionTextarea).val('');

          Toast.fire({
            icon: 'success',
            title: 'Comentário criado com sucesso.'
          });
        })
        .catch(err => {
          Toast.fire({
            icon: 'error',
            title: 'Houve um erro ao criar o comentário. Tente novamente!'
          });
        })
        .finally(() => {
          $(commentDescriptionTextarea).removeAttr('disabled');
          $(addCommentButton).removeAttr('disabled');

          $(addCommentButton).html(`Comentar`);
        });
    });
  }


  // Meetings
  function initFlatpickrFields() {
    $('#tcc_meeting_datetime').flatpickr({
      enableTime: true,
      dateFormat: "d/m/Y H:i",
      time_24hr: true,
      allowInput: true,
    });
  }

  function addErrorInField(error, id) {
    $(id).addClass('is-invalid');
    if (Array.isArray(error)) {
      error.forEach(err => {
        $(id).parent().append(`
          <div class="invalid-feedback">
            ${err}
          </div>
        `);
      });
    } else {
      $(id).parent().append(`
        <div class="invalid-feedback">
          ${error}
        </div>
      `);
    }
  }

  function handleModalFormError(data) {
    if (data.description) {
      addErrorInField(data.description, '#tcc_meeting_description');
    }

    if (data.meeting_date) {
      addErrorInField(data.meeting_date, '#tcc_meeting_datetime');
    }
  }

  function removeErrorInField(id) {
    $(id).removeClass('is-invalid');
    $(id).parent().find('.invalid-feedback').remove();
  }

  function resetModalFormError() {
    removeErrorInField('#tcc_meeting_description');
    removeErrorInField('#tcc_meeting_datetime');
  }

  function handleRequestMeetingEvent() {
    $(modal.requestButton).click(() => {
      modal.object.show();
    })
  }

  function handleRequestMeetingConfirmEvent() {
    $(modal.confirmButton).click(function(e) {
      $(modal.cancelButton).attr('disabled', true);
      $(modal.confirmButton).attr('disabled', true);
      $(modal.closeButton).attr('disabled', true);
      $(modal.confirmButton).html(`
        <div class="spinner-border spinner-border-sm text-white me-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        Solicitar
      `);

      let fetchResponse;

      API.meetings.add($('#tcc_meeting_description').val(), )
        .then(response => fetchResponse = response)
        .then(response => response.json())
        .then(data => {
          if (fetchResponse.status >= 300) {
            resetModalFormError();
            handleModalFormError(data);
          } else {
            getAllMeetings();
            modal.object.hide();

            $('#tcc_meeting_description').val('');
            $('#tcc_meeting_datetime').val('');

            Toast.fire({
              icon: 'success',
              title: 'Reunião requisitada com sucesso.'
            });
          }
        })
        .catch((err) => {
          console.log(err);
          Toast.fire({
            icon: 'error',
            title: 'Houve um erro no servidor. Tente novamente!'
          });
        })
        .finally(() => {
          $(modal.cancelButton).removeAttr('disabled');
          $(modal.confirmButton).removeAttr('disabled');
          $(modal.closeButton).removeAttr('disabled');
          $(modal.confirmButton).html(`
            Solicitar
          `);
        });
    });
  }

  function getAllMeetings() {
    API.meetings.list()
      .then(response => response.json())
      .then(response => {
        let meetings = '';

        if (response.length == 0) {
          $(meetingsContainer).html(`
            <div class="p-4 border rounded">
              <div class="mt-2">
                <p class="mb-0">
                  Sem reuniões
                </p>
              </div>
            </div>
          `);

          return;
        }

        response.forEach(meeting => {
          let chip = `
            <span class="badge badge-sm badge-light">
              Pendente
            </span>
          `;

          if (meeting.is_approved == true) {
            chip = `
              <span class="badge badge-sm badge-light-success">
                Aprovado
              </span>
            `;
          } else if (meeting.is_approved == false) {
            chip = `
              <span class="badge badge-sm badge-light-danger">
                Reprovado
              </span>
            `;
          }

          meetings += `
            <div class="p-4 border rounded mt-2">
              <div class="d-flex justify-content-between text-gray-500">
                <div class="d-flex">
                  ${
                    meeting.participants.map(participant => {
                      let badge = `
                        <i
                          class="fas fa-minus-circle fa-fw fs-4 text-dark-light ms-2"
                          data-bs-toggle="tooltip"
                          data-bs-placement="top"
                          title="Pendente"></i>
                      `;

                      if (participant.approved == true) {
                        badge = `
                          <i
                            class="fas fa-check-circle fa-fw fs-4 text-success ms-2"
                            data-bs-toggle="tooltip"
                            data-bs-placement="top"
                            title="Aprovado"></i>
                        `;
                      } else if (participant.approved == false) {
                        badge = `
                          <i
                            class="fas fa-times-circle fa-fw fs-4 text-danger ms-2"
                            data-bs-toggle="tooltip"
                            data-bs-placement="top"
                            title="Reprovado"></i>
                        `;
                      }

                      return `
                        <div class="me-8 d-flex flex-row align-items-center">
                          <h5 class="mb-0">
                            ${participant.user_detail.full_name}
                          </h5>

                          ${badge}
                        </div>
                      `;
                    }).join('')
                  }
                </div>

                <div>
                  <span class="me-2">
                    ${meeting.meeting_date}
                  </span>

                  ${chip}
                </div>
              </div>
              <div class="mt-2">
                <p class="mb-0">
                  ${meeting.description}
                </p>
              </div>
            </div>
          `;
        });
        $(meetingsContainer).html(meetings);
      });
  }


  getElements();
  initFlatpickrFields();

  initAddCommentEvent();

  handleRequestMeetingEvent();
  handleRequestMeetingConfirmEvent();

  getAllMeetings();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkStageDetail();
});
