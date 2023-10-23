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

  let changeRequestModal = {
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
      edit(meeting, developedActivities, instructions) {
        return fetch(`/api/meetings/${meeting}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            developed_activities: developedActivities,
            instructions: instructions,
          }),
        });
      },
      approve(meeting) {
        return fetch('/api/meetings/approve/', {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            meeting,
          }),
        })
      },
      disapprove(meeting) {
        return fetch('/api/meetings/disapprove/', {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            meeting,
          }),
        })
      },
    },
    workStages: {
      requestReview(workStage) {
        return fetch(`/api/final-work-stages/${workStage}/request_review/`, {
          method: 'get',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      markReviewed(workStage) {
        return fetch(`/api/final-work-stages/${workStage}/mark_reviewed/`, {
          method: 'get',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      markCompleted(workStage) {
        return fetch(`/api/final-work-stages/${workStage}/mark_completed/`, {
          method: 'get',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      markPresented(workStage) {
        return fetch(`/api/final-work-stages/${workStage}/mark_presented/`, {
          method: 'get',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
    },
    changeRequests: {
      add(description, workStage) {
        return fetch(`/api/change-requests/`, {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            description: description,
            work_stage: workStage,
          }),
        });
      },
    },
  };

  function handleCommetMaxLengthBadge() {
    $('#tcc_comment_textarea').maxlength({
      warningClass: "badge badge-warning z-index-2000",
      limitReachedClass: "badge badge-success z-index-2000"
    });
  }

  function handleMeetingModalMaxLengthBadge () {
    $('#tcc_meeting_description').maxlength({
      warningClass: "badge badge-warning z-index-2000",
      limitReachedClass: "badge badge-success z-index-2000"
    });
  }

  function handleCommentFormValidator() {
    $('#tcc_comment_form').validate({
      errorElement: 'div',
      errorClass: 'invalid-feedback',
      highlight: function(element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      },
      rules: {
        comment: {
          required: true,
          minlength: 3,
          maxlength: 255
        },
      },
      messages: {
        comment: {
          required: 'O comentário deve ser inserida.',
          minlength: 'O comentário deve ter pelo menos 3 caracteres.',
          maxlength: 'O comentário não pode ter mais de 255 caracteres.'
        },
      },
    });

    $('#tcc_comment_textarea').keyup(function(e) {
      $(this).valid();
    });
  }

  function handleMeetingModalValidator() {
    $('#tcc_request_meeting_form').validate({
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
        meeting_date: {
          required: true,
        },
      },
      messages: {
        description: {
          required: 'A descrição deve ser inserida.',
          minlength: 'A descrição deve ter pelo menos 3 caracteres.',
          maxlength: 'A descrição não pode ter mais de 255 caracteres.'
        },
        meeting_date: {
          required: 'A data da reunião deve ser inserida.',
        }
      },
    });

    $('#tcc_meeting_description').keyup(function(e) {
      $(this).valid();
    });
  }

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
    changeRequestModal.element = $('#tcc_change_request_modal');
    changeRequestModal.object = new bootstrap.Modal(changeRequestModal.element);
    changeRequestModal.requestButton = $('#tcc_change_request_button');
    changeRequestModal.cancelButton = $('#tcc_change_request_modal_cancel');
    changeRequestModal.confirmButton = $('#tcc_change_request_modal_confirm');
    changeRequestModal.closeButton = $('#tcc_change_request_modal_close');
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
              <div>
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
    $('#tcc_comment_form').submit(function (e) {
      e.preventDefault();

      if (!$(this).valid()) {
        return;
      }

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
      altInput: true,
      altFormat: "d/m/Y H:i",
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
    $('#tcc_request_meeting_form').submit(function(e) {
      e.preventDefault();

      if (!$(this).valid()) {
        return;
      }

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

      API.meetings.add($('#tcc_meeting_description').val(), $('#tcc_meeting_datetime').val())
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
              <div>
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

          let footer = ``;
          let supervisorForm = ``;

          if (meeting.required_review) {
            footer = `
              <div class="mt-2 d-flex flex-column flex-sm-row justify-content-end">
                <button
                  type="button"
                  class="btn btn-sm btn-light me-2 tcc_meeting_requested_disapprove w-100 w-sm-auto">
                  Recusar
                </button>

                <button
                  type="button"
                  class="btn btn-sm btn-primary tcc_meeting_requested_approve w-100 w-sm-auto mt-2 mt-sm-0">
                  Aprovar
                </button>
              </div>
            `;
          }

          if (meeting.is_approved) {
            if (meetingsContainer.data('supervisor')) {
              supervisorForm = `
                <div>
                  <form class="tcc_meeting_supervisor_form_${meeting.id}">
                    <div class="fv-row mt-4 mb-8">
                      <label for="developed_activities_${meeting.id}" class="required form-label">
                        Atividades desenvolvidas
                      </label>
  
                      <textarea
                        id="tcc_developed_activities_${meeting.id}"
                        class="form-control form-control-solid tcc_developed_activities_field_${meeting.id}"
                        name="developed_activities_${meeting.id}"
                        cols="30"
                        rows="10"
                        minlength="3"
                        maxlength="255">${meeting.developed_activities}</textarea>
                    </div>
  
                    <div class="fv-row mb-8">
                      <label for="instructions_${meeting.id}" class="required form-label">
                        Instruções
                      </label>
  
                      <textarea
                        id="tcc_instructions_${meeting.id}"
                        class="form-control form-control-solid tcc_instructions_field_${meeting.id}"
                        name="instructions_${meeting.id}"
                        cols="30"
                        rows="10"
                        minlength="3"
                        maxlength="255">${meeting.instructions}</textarea>
                    </div>
  
                    <div class="d-flex mt-4 justify-content-end">
                      <button class="btn btn-sm btn-primary w-100 w-sm-auto tcc_meeting_supervisor_confirm_${meeting.id}">
                        Salvar
                      </button>
                    </div>
                  </form>
                </div>
              `;
            } else {
              supervisorForm = `
                <div>
                  <div class="fv-row mt-4 mb-8">
                    <label class="required form-label">
                      Atividades desenvolvidas
                    </label>
  
                    <textarea
                      class="form-control form-control-solid disabled"
                      cols="30"
                      rows="10"
                      minlength="3"
                      maxlength="255"
                      disabled>${meeting.developed_activities}</textarea>
                  </div>
  
                  <div class="fv-row">
                    <label class="required form-label">
                      Instruções
                    </label>
  
                    <textarea
                      class="form-control form-control-solid disabled"
                      cols="30"
                      rows="10"
                      minlength="3"
                      maxlength="255"
                      disabled>${meeting.instructions}</textarea>
                  </div>
                </div>
              `;
            }
          }

          meetings += `
            <div class="p-4 border rounded mt-2 tcc_requested_meeting_item" data-meeting="${meeting.id}">
              <div class="d-flex flex-wrap flex-column flex-sm-row justify-content-between text-gray-500">
                <div class="d-flex flex-column flex-sm-row flex-wrap mb-0 mb-sm-2">
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
                        <div class="me-8 mb-2 mb-sm-0 d-flex flex-row align-items-center">
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
                    ${meeting.meeting_date_formated}
                  </span>

                  ${chip}
                </div>
              </div>
              <div class="mt-2">
                <p class="mb-0">
                  ${meeting.description}
                </p>
              </div>

              ${footer}

              ${supervisorForm}
            </div>
          `;
        });
        $(meetingsContainer).html(meetings);
      })
      .then(() => {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl);
        });
      })
      .then(() => {
        handleMettingApproveButton();
        handleMettingDisapproveButton();
      });
  }

  function handleMettingDisapproveButton() {
    $('.tcc_meeting_requested_disapprove').click(function(e) {
      Swal.fire({
        title: 'Reprovar reunião',
        text: 'Tem certeza que deseja reprovar esta reunião?',
        icon: 'warning',
        customClass: {
          actions: 'my-actions',
          cancelButton: 'btn btn-secondary order-1',
          confirmButton: 'btn btn-primary order-2',
        },
        buttonsStyling: false,
        showCancelButton: true,
        confirmButtonText: 'Confirmar'
      }).then(result => {
        const { isConfirmed } = result;
  
        const id = $(this).parent().parent().data('meeting');

        if (isConfirmed) {
          API.meetings.disapprove(id)
            .then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }  
            }).then(() => {
              Toast.fire({
                icon: 'success',
                title: 'Reunião reprovado com sucesso.'
              });

              getAllMeetings();
            }).catch(err => {
              Toast.fire({
                icon: 'error',
                title: 'Houve um erro no servidor.'
              });
            });
        }
      });
    });
  }

  function handleMettingApproveButton() {
    $('.tcc_meeting_requested_approve').click(function(e) {
      Swal.fire({
        title: 'Aprovar reunião',
        text: 'Tem certeza que deseja aprovar esta reunião?',
        icon: 'warning',
        customClass: {
          actions: 'my-actions',
          cancelButton: 'btn btn-secondary order-1',
          confirmButton: 'btn btn-primary order-2',
        },
        buttonsStyling: false,
        showCancelButton: true,
        confirmButtonText: 'Confirmar'
      }).then(result => {
        const { isConfirmed } = result;
  
        const id = $(this).parent().parent().data('meeting');

        if (isConfirmed) {
          API.meetings.approve(id)
            .then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }  
            }).then(() => {
              Toast.fire({
                icon: 'success',
                title: 'Reunião aprovada com sucesso.'
              });

              getAllMeetings();
            }).catch(err => {
              Toast.fire({
                icon: 'error',
                title: 'Houve um erro no servidor.'
              });
            });
        }
      });
    });
  }

  function handleMeetingSupervisorForm() {
    $('[class*="tcc_meeting_supervisor_confirm_"]').click(function(e) {
      const form = $(this).parent().parent();
      const valid = $(form).valid();

      const id = $(form).attr('class').split('tcc_meeting_supervisor_form_')[1];

      if (valid) {
        const developedActivities = $(form).find(`#tcc_developed_activities_${id}`).val();
        const instructions = $(form).find(`#tcc_instructions_${id}`).val();

        API.meetings.edit(id, developedActivities, instructions)
          .then(response => {
            if (response.ok === false) {
              throw new Error(response.statusText);
            }
          }).then(() => {
            Toast.fire({
              icon: 'success',
              title: 'Reunião atualizada com sucesso.'
            });
          }).catch(err => {
            Toast.fire({
              icon: 'error',
              title: 'Houve um erro no servidor.'
            });
          });
      }
    });
  }

  function handleMeetingFormValidator() {
    $('[class*="tcc_meeting_supervisor_form_"]').submit(function(e) {
      e.preventDefault();
    });

    $('[class*="tcc_meeting_supervisor_form_"]').each(function(index, element) {
      const id = $(element).attr('class').split('tcc_meeting_supervisor_form_')[1];

      const rules = {};
      const messages = {};

      const developedActivities = `developed_activities_${id}`;
      const instructions = `instructions_${id}`;

      rules[developedActivities] = {
        required: true,
        minlength: 3,
        maxlength: 255
      };
      rules[instructions] = {
        required: true,
        minlength: 3,
        maxlength: 255
      };

      messages[developedActivities] = {
        required: 'As atividades desenvolvidas devem ser inserida.',
        minlength: 'O campo de atividades deve ter pelo menos 3 caracteres.',
        maxlength: 'O campo de atividades não pode ter mais de 255 caracteres.'
      };
      messages[instructions] = {
        required: 'As instrunções desenvolvidas devem ser inserida.',
        minlength: 'O campo de instrunções deve ter pelo menos 3 caracteres.',
        maxlength: 'O campo de instrunções não pode ter mais de 255 caracteres.'
      };

      $(element).validate({
        errorElement: 'div',
        errorClass: 'invalid-feedback',
        highlight: function(element, errorClass, validClass) {
          $(element).addClass('is-invalid');
        },
        unhighlight: function(element, errorClass, validClass) {
          $(element).removeClass('is-invalid');
        },
        rules,
        messages,
      });

      $(`[name="${developedActivities}"]`).keyup(function(e) {
        $(this).valid();
      });

      $(`[name="${instructions}"]`).keyup(function(e) {
        $(this).valid();
      });
    });
  }

  function addMeetingFormBootstrapMaxLength() {
    $('[class*="tcc_developed_activities_field_"]').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });

    $('[class*="tcc_instructions_field_"]').maxlength({
      warningClass: "badge badge-warning",
      limitReachedClass: "badge badge-success"
    });
  }


  // Request review
  function handleRequestReviewButton() {
    $('#tcc_request_review_button').click(function(e) {
      Swal.fire({
        title: 'Solicitar correção',
        text: 'Tem certeza que deseja solicitar uma correção?',
        icon: 'warning',
        customClass: {
          actions: 'my-actions',
          cancelButton: 'btn btn-secondary order-1',
          confirmButton: 'btn btn-primary order-2',
        },
        buttonsStyling: false,
        showCancelButton: true,
        confirmButtonText: 'Confirmar'
      }).then(result => {
        const { isConfirmed } = result;
  
        const id = $('#kt_content_container').data('work-stage');

        if (isConfirmed) {
          API.workStages.requestReview(id)
            .then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }  
            }).then(() => {
              let currentUrl = window.location.href;

              let hasQueryParams = currentUrl.includes('?');

              let newParam = 'success_review_request=true';

              let newUrl;
              if (hasQueryParams) {
                newUrl = currentUrl + '&' + newParam;
              } else {
                newUrl = currentUrl + '?' + newParam;
              }

              window.location.href = newUrl;
            }).catch(err => {
              console.log(err);

              Toast.fire({
                icon: 'error',
                title: 'Houve um erro no servidor.'
              });
            });
        }
      });
    });
  }


  // Mark Reviewed
  function handleMarkReviewedButton() {
    $('#tcc_mark_reviewed_button').click(function(e) {
      Swal.fire({
        title: 'Marcar como corrigido',
        text: 'Tem certeza que deseja marcar como corrigido esta etapa?',
        icon: 'warning',
        customClass: {
          actions: 'my-actions',
          cancelButton: 'btn btn-secondary order-1',
          confirmButton: 'btn btn-primary order-2',
        },
        buttonsStyling: false,
        showCancelButton: true,
        confirmButtonText: 'Confirmar'
      }).then(result => {
        const { isConfirmed } = result;
  
        const id = $('#kt_content_container').data('work-stage');

        if (isConfirmed) {
          API.workStages.markReviewed(id)
            .then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }  
            }).then(() => {
              let currentUrl = window.location.href;

              let hasQueryParams = currentUrl.includes('?');

              let newParam = 'success_mark_reviewed=true';

              let newUrl;
              if (hasQueryParams) {
                newUrl = currentUrl + '&' + newParam;
              } else {
                newUrl = currentUrl + '?' + newParam;
              }

              window.location.href = newUrl;
            }).catch(err => {
              console.log(err);

              Toast.fire({
                icon: 'error',
                title: 'Houve um erro no servidor.'
              });
            });
        }
      });
    });
  }


  // Completed
  function handleCompleteButton() {
    $('#tcc_complete_button').click(function(e) {
      Swal.fire({
        title: 'Marcar como concluído',
        text: 'Tem certeza que deseja marcar como concluído esta etapa?',
        icon: 'warning',
        customClass: {
          actions: 'my-actions',
          cancelButton: 'btn btn-secondary order-1',
          confirmButton: 'btn btn-primary order-2',
        },
        buttonsStyling: false,
        showCancelButton: true,
        confirmButtonText: 'Confirmar'
      }).then(result => {
        const { isConfirmed } = result;
  
        const id = $('#kt_content_container').data('work-stage');

        if (isConfirmed) {
          API.workStages.markCompleted(id)
            .then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }  
            }).then(() => {
              let currentUrl = window.location.href;

              let hasQueryParams = currentUrl.includes('?');

              let newParam = 'success_mark_completed=true';

              let newUrl;
              if (hasQueryParams) {
                newUrl = currentUrl + '&' + newParam;
              } else {
                newUrl = currentUrl + '?' + newParam;
              }

              window.location.href = newUrl;
            }).catch(err => {
              console.log(err);

              Toast.fire({
                icon: 'error',
                title: 'Houve um erro no servidor.'
              });
            });
        }
      });
    });
  }


  // Mark Completed
  function handleMarkCompletedButton() {
    $('#tcc_mark_completed_button').click(function(e) {
      Swal.fire({
        title: 'Marcar como concluído',
        text: 'Tem certeza que deseja marcar como concluído esta etapa?',
        icon: 'warning',
        customClass: {
          actions: 'my-actions',
          cancelButton: 'btn btn-secondary order-1',
          confirmButton: 'btn btn-primary order-2',
        },
        buttonsStyling: false,
        showCancelButton: true,
        confirmButtonText: 'Confirmar'
      }).then(result => {
        const { isConfirmed } = result;
  
        const id = $('#kt_content_container').data('work-stage');

        if (isConfirmed) {
          API.workStages.markCompleted(id)
            .then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }  
            }).then(() => {
              let currentUrl = window.location.href;

              let hasQueryParams = currentUrl.includes('?');

              let newParam = 'success_mark_completed=true';

              let newUrl;
              if (hasQueryParams) {
                newUrl = currentUrl + '&' + newParam;
              } else {
                newUrl = currentUrl + '?' + newParam;
              }

              window.location.href = newUrl;
            }).catch(err => {
              console.log(err);

              Toast.fire({
                icon: 'error',
                title: 'Houve um erro no servidor.'
              });
            });
        }
      });
    });
  }

  function handleMarkPresentedButton() {
    $('#tcc_mark_presented_button').click(function(e) {
      Swal.fire({
        title: 'Marcar como apresentado',
        text: 'Tem certeza que deseja marcar como apresentado esta etapa?',
        icon: 'warning',
        customClass: {
          actions: 'my-actions',
          cancelButton: 'btn btn-secondary order-1',
          confirmButton: 'btn btn-primary order-2',
        },
        buttonsStyling: false,
        showCancelButton: true,
        confirmButtonText: 'Confirmar'
      }).then(result => {
        const { isConfirmed } = result;
  
        const id = $('#kt_content_container').data('work-stage');

        if (isConfirmed) {
          API.workStages.markPresented(id)
            .then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }  
            }).then(() => {
              let currentUrl = window.location.href;

              let hasQueryParams = currentUrl.includes('?');

              let newParam = 'success_mark_presented=true';

              let newUrl;
              if (hasQueryParams) {
                newUrl = currentUrl + '&' + newParam;
              } else {
                newUrl = currentUrl + '?' + newParam;
              }

              window.location.href = newUrl;
            }).catch(err => {
              console.log(err);

              Toast.fire({
                icon: 'error',
                title: 'Houve um erro no servidor.'
              });
            });
        }
      });
    });
  }


  // Request change
  function handleChangeRequestEvent() {
    $(changeRequestModal.requestButton).click(() => {
      changeRequestModal.object.show();
    })
  }

  function resetChangeRequestModalFormError() {
    removeErrorInField('#tcc_change_description');
  }

  function handleChangeRequestModalFormError(data) {
    if (data.description) {
      addErrorInField(data.description, '#tcc_change_description');
    }
  }

  function handleChangeRequestConfirmEvent() {
    $(changeRequestModal.confirmButton).click(function(e) {
      $(changeRequestModal.cancelButton).attr('disabled', true);
      $(changeRequestModal.confirmButton).attr('disabled', true);
      $(changeRequestModal.closeButton).attr('disabled', true);
      $(changeRequestModal.confirmButton).html(`
        <div class="spinner-border spinner-border-sm text-white me-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        Solicitar
      `);

      let fetchResponse;

      const id = $('#kt_content_container').data('work-stage');

      API.changeRequests.add($('#tcc_change_description').val(), id)
        .then(response => fetchResponse = response)
        .then(response => response.json())
        .then(data => {
          if (fetchResponse.status >= 300) {
            resetChangeRequestModalFormError();
            handleChangeRequestModalFormError(data);
          } else {
            changeRequestModal.object.hide();

            $('#tcc_change_description').val('');

            let currentUrl = window.location.href;

            let hasQueryParams = currentUrl.includes('?');

            let newParam = 'success_change_request=true';

            let newUrl;
            if (hasQueryParams) {
              newUrl = currentUrl + '&' + newParam;
            } else {
              newUrl = currentUrl + '?' + newParam;
            }

            window.location.href = newUrl;
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
          $(changeRequestModal.cancelButton).removeAttr('disabled');
          $(changeRequestModal.confirmButton).removeAttr('disabled');
          $(changeRequestModal.closeButton).removeAttr('disabled');
          $(changeRequestModal.confirmButton).html(`
            Solicitar
          `);
        });
    });
  }


  getElements();

  handleMeetingModalValidator();
  handleMeetingModalMaxLengthBadge();

  handleCommetMaxLengthBadge();
  handleCommentFormValidator();

  initFlatpickrFields();
  initAddCommentEvent();

  handleRequestMeetingEvent();
  handleRequestMeetingConfirmEvent();
  handleMettingApproveButton();
  handleMettingDisapproveButton();
  handleMeetingSupervisorForm();
  handleMeetingFormValidator();
  addMeetingFormBootstrapMaxLength();

  handleRequestReviewButton();
  handleMarkReviewedButton();
  handleMarkCompletedButton();
  handleMarkPresentedButton();
  handleCompleteButton();

  handleChangeRequestEvent();
  handleChangeRequestConfirmEvent();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkStageDetail();
});
