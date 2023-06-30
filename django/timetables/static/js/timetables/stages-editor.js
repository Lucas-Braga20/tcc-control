class StageEditor {
  container = null;

  addButton = null;

  // Modal
  modal = {
    element: null,
    object: null,
    cancelButton: null,
    confirmButton: null,
  };

  items = new Array();

  API = {
    stages: {
      list() {
        return fetch(`/api/stages/?no_page=true`, {
          method: 'get',
          headers: {
            'Content-Type': 'application/json',
          },
        });
      },
      create(body) {
        return fetch(`/api/stages/`, {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
        });
      },
      delete(id) {
        return fetch(`/api/stages/${id}/`, {
          method: 'delete',
          headers: {
            'Content-Type': 'application/json',
          },
        })
      },
    },
  };


  // Handle fields inside collapse.
  generateDescriptionFieldElement(id) {
    const elementId = `tcc_stage_editor_description_${id}`;

    return `
      <div class="fv-row mb-8">
        <label for="${elementId}" class="required form-label">Descrição</label>
        <input
          id="${elementId}"
          type="text"
          class="form-control form-control-solid tcc_description_field"
          placeholder="Descrição">
      </div>
    `;
  }

  generateActivityFieldElement(id) {
    const elementId = `tcc_stage_editor_activity_${id}`;

    return `
      <div class="fv-row mb-8">
        <label for="${elementId}" class="required form-label">Configuração de atividade</label>
        <select id="${elementId}" class="form-select form-select-solid tcc_activity_field">
        </select>
      </div>
    `;
  }

  generateStartDateFieldElement(id) {
    const elementId = `tcc_stage_editor_start_date_${id}`;

    return `
      <div class="fv-row mb-8">
        <label for="${elementId}" class="required form-label">Data de início</label>
        <input
          class="form-control form-control-solid"
          placeholder="dd/mm/aaaa"
          id="${elementId}"/>
      </div>
    `;
  }

  generateSupervisorDateFieldElement(id) {
    const elementId = `tcc_stage_editor_supervisor_date_${id}`;

    return `
      <div class="fv-row mb-8">
        <label for="${elementId}" class="required form-label">Data de envio ao supervisor</label>
        <input
          class="form-control form-control-solid"
          placeholder="dd/mm/aaaa"
          id="${elementId}"/>
      </div>
    `;
  }

  generateSendDateFieldElement(id) {
    const elementId = `tcc_stage_editor_send_date_${id}`;

    return `
      <div class="fv-row mb-8">
        <label for="${elementId}" class="required form-label">Data de envio</label>
        <input
          class="form-control form-control-solid"
          placeholder="dd/mm/aaaa"
          id="${elementId}"/>
      </div>
    `;
  }

  generatePresentationDateFieldElement(id) {
    const elementId = `tcc_stage_editor_presentation_date_${id}`;

    return `
      <div class="fv-row mb-8">
        <label for="${elementId}" class="form-label">Data de apresentação</label>
        <input
          class="form-control form-control-solid"
          placeholder="dd/mm/aaaa"
          id="${elementId}"/>
      </div>
    `;
  }

  initFieldElements(stage) {
    $(`#tcc_stage_editor_activity_${stage.id}`).select2({
      ajax: {
        url: '/api/activities/',
        dataType: 'json',
        data: function ({ term }, page) {
          return {
            search: term,
          };
        },
        processResults: function (data) {
          return {
            results: data.results.map(activity => {
              return {
                id: activity.id,
                text: activity.name,
              };
            }),
          };
        },
        cache: true,
      },
      closeOnSelect: true,
      placeholder: 'Selecione a configuração de atividade'
    });

    $.ajax({
      url: `/api/activities/${stage.activity_configuration}/`,
      dataType: 'json',
      success: function(data) {
        const option = new Option(data.name, data.id, true, true);
        $(`#tcc_stage_editor_activity_${stage.id}`).append(option).trigger('change');
      }
    });

    $(`#tcc_stage_editor_start_date_${stage.id}`).flatpickr({
      dateFormat: 'd/m/Y',
      defaultDate: moment(stage.start_date).format('DD/MM/YYYY'),
    });

    $(`#tcc_stage_editor_supervisor_date_${stage.id}`).flatpickr({
      dateFormat: 'd/m/Y',
      defaultDate: moment(stage.send_date_supervisor).format('DD/MM/YYYY'),
    });

    $(`#tcc_stage_editor_send_date_${stage.id}`).flatpickr({
      dateFormat: 'd/m/Y',
      defaultDate: moment(stage.send_date).format('DD/MM/YYYY'),
    });

    $(`#tcc_stage_editor_presentation_date_${stage.id}`).flatpickr({
      dateFormat: 'd/m/Y',
      defaultDate: moment(stage.presentation_date).format('DD/MM/YYYY'),
    });

    $(`#tcc_stage_editor_description_${stage.id}`).val(stage.description);
  }

  initModalFieldElements() {
    $(`#tcc_stage_editor_activity`).select2({
      ajax: {
        url: '/api/activities/',
        dataType: 'json',
        data: function ({ term }, page) {
          return {
            search: term,
          };
        },
        processResults: function (data) {
          return {
            results: data.results.map(activity => {
              return {
                id: activity.id,
                text: activity.name,
              };
            }),
          };
        },
        cache: true,
      },
      closeOnSelect: true,
      placeholder: 'Selecione a configuração de atividade'
    });

    $(`#tcc_stage_editor_start_date`).flatpickr({
      dateFormat: 'd/m/Y',
    });

    $(`#tcc_stage_editor_supervisor_date`).flatpickr({
      dateFormat: 'd/m/Y',
    });

    $(`#tcc_stage_editor_send_date`).flatpickr({
      dateFormat: 'd/m/Y',
    });

    $(`#tcc_stage_editor_presentation_date`).flatpickr({
      dateFormat: 'd/m/Y',
    });
  }


  // Manipulate elements in list.
  addItemElementToList(stage) {
    $(this.container).append(`
      <div id="tcc_accordion-item_${stage.id}" class="accordion-item">
        <h2 class="accordion-header" id="tcc_accordion_header_${stage.id}">
          <button
            class="accordion-button fs-4 fw-bold collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#tcc_accordion_body_${stage.id}"
            aria-expanded="true"
            aria-controls="tcc_accordion_body_${stage.id}">
            <div class="d-flex justify-content-between w-100">
              <div>
                <h3 class="mb-0 fs-6 text-dark">
                  Descrição:
                  <span class="fw-light">
                    ${stage.description}
                  </span>
                </h3>
              </div>
              <div class="me-3">
                <p class="mb-0 fs-6 text-dark">
                  Data de início:
                  <span class="text-muted">
                    ${moment(stage.start_date).format('DD/MM/YYYY')}
                  </span>
                </p>
              </div>
            </div>
          </button>
        </h2>
        <div
          id="tcc_accordion_body_${stage.id}"
          class="accordion-collapse collapse"
          aria-labelledby="tcc_accordion_header_${stage.id}"
          data-bs-parent="#tcc_stage_editor_container">
          <div class="accordion-body">
            ${this.generateDescriptionFieldElement(stage.id)}
            ${this.generateActivityFieldElement(stage.id)}
            ${this.generateStartDateFieldElement(stage.id)}
            ${this.generateSupervisorDateFieldElement(stage.id)}
            ${this.generateSendDateFieldElement(stage.id)}
            ${this.generatePresentationDateFieldElement(stage.id)}

            <div class="d-flex justify-content-end">
              <div>
                <button type="button" class="btn btn-sm btn-danger tcc_remove_button" data-id="${stage.id}">Remover</button>
              </div>
              <div class="ms-2">
                <button type="button" class="btn btn-sm btn-primary tcc_save_button" data-id="${stage.id}">Salvar</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `);

    this.initFieldElements(stage);
  }
  
  turnOnLoadingState() {
    $(this.container).html(`
      <div class="d-flex justify-content-center align-items-center py-3">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <span class="ms-3">Carregando campos...</span>
      </div>
    `);
  }


  // Modal Events
  handleAddButton() {
    $(this.addButton).click(() => {
      this.modal.object.show();
    })
  }

  handleModalCloseEvent() {
    const ctx = this;

    $(this.modal.element).on('hidden.bs.modal', function(e) {
      ctx.resetModalFormError();
      ctx.resetModalFormValues();
    });
  }

  handleModalConfirmButton() {
    $(this.modal.confirmButton).click(() => {
      $(this.modal.cancelButton).html(`
        <div class="d-flex align-items-center">
          <div class="spinner-border spinner-border-sm text-light me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          Fechar
        </div>
      `).attr('disabled', true);
      $(this.modal.confirmButton).html(`
        <div class="d-flex align-items-center">
          <div class="spinner-border spinner-border-sm text-primary me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          Confirmar
        </div>
      `).attr('disabled', true);

      let fetchResponse;
      let ctx = this;

      this.API.stages.create({
        description: $('#tcc_stage_editor_description').val(),
        activity_configuration: $('#tcc_stage_editor_activity').val(),
        start_date: getDatetimeFormat($('#tcc_stage_editor_start_date').val()),
        send_date_supervisor: getDatetimeFormat($('#tcc_stage_editor_supervisor_date').val()),
        send_date: getDatetimeFormat($('#tcc_stage_editor_send_date').val()),
        presentation_date: getDatetimeFormat($('#tcc_stage_editor_presentation_date').val()),
        timetable: $(ctx.container).data('timetable'),
      })
        .then(response => fetchResponse = response)
        .then(response => response.json())
        .then(data => {
          if (fetchResponse.status >= 300) {
            ctx.resetModalFormError();
            ctx.handleModalFormError(data);
          } else {
            ctx.getStageList();
            ctx.modal.object.hide();
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
          $(this.modal.cancelButton).html(`
            Fechar
          `).removeAttr('disabled');
          $(this.modal.confirmButton).html(`
            Confirmar
          `).removeAttr('disabled');
        });
    });
  }

  handleModalFormError(data) {
    if (data.description) {
      this.addErrorInField(data.description, '#tcc_stage_editor_description');
    }

    if (data.activity_configuration) {
      this.addErrorInField(data.activity_configuration, '#tcc_stage_editor_activity');
    }

    if (data.start_date) {
      this.addErrorInField(data.start_date, '#tcc_stage_editor_start_date');
    }

    if (data.send_date_supervisor) {
      this.addErrorInField(data.send_date_supervisor, '#tcc_stage_editor_supervisor_date');
    }

    if (data.send_date) {
      this.addErrorInField(data.send_date, '#tcc_stage_editor_send_date');
    }

    if (data.presentation_date) {
      this.addErrorInField(data.presentation_date, '#tcc_stage_editor_presentation_date');
    }
  }

  addErrorInField(error, id) {
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

  resetModalFormError() {
    this.removeErrorInField('#tcc_stage_editor_description');
    this.removeErrorInField('#tcc_stage_editor_activity');
    this.removeErrorInField('#tcc_stage_editor_start_date');
    this.removeErrorInField('#tcc_stage_editor_supervisor_date');
    this.removeErrorInField('#tcc_stage_editor_send_date');
    this.removeErrorInField('#tcc_stage_editor_presentation_date');
  }

  resetModalFormValues() {
    $('#tcc_stage_editor_description').val('');
    $('#tcc_stage_editor_activity').val(null).trigger('change');
    $('#tcc_stage_editor_start_date').get(0)._flatpickr.clear();
    $('#tcc_stage_editor_supervisor_date').get(0)._flatpickr.clear();
    $('#tcc_stage_editor_send_date').get(0)._flatpickr.clear();
    $('#tcc_stage_editor_presentation_date').get(0)._flatpickr.clear();
  }

  removeErrorInField(id) {
    $(id).removeClass('is-invalid');
    $(id).parent().find('.invalid-feedback').remove();
  }


  // Collapse Events
  handleCollapseRemoveButton() {
    const ctx = this;

    $('.tcc_remove_button').click(function (e) {
      Swal.fire({
        title: 'Remover etapa',
        text: 'Tem certeza que deseja remover esta etapa?',
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

        if (isConfirmed) {
          ctx.API.stages.delete($(this).data('id'))
            .then(response => {
              if (response.status >= 300) {
                throw new Error();
              }
            })
            .then(() => {
              Toast.fire({
                icon: 'success',
                title: 'Etapa removida com sucesso.'
              });

              ctx.getStageList();
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


  // Get HTML elements.
  getElements() {
    try {
      this.container = document.getElementById('tcc_stage_editor_container');
      this.addButton = document.getElementById('tcc_stage_editor_add_btn');
      this.modal.element = document.getElementById('tcc_modal_stage');
      this.modal.object = new bootstrap.Modal(this.modal.element);
      this.modal.cancelButton = document.getElementById('tcc_stage_editor_modal_cancel_button');
      this.modal.confirmButton = document.getElementById('tcc_stage_editor_modal_confirm_button');
    } catch (err) {
      console.log(err)
      throw new Error('Activity Fields Editor - Cannot find elements.');
    }
  }

  getStageList() {
    this.turnOnLoadingState();

    this.API.stages.list()
      .then(response => response.json())
      .then(response => {
        $(this.container).html('');

        response.forEach(stage => {
          this.addItemElementToList(stage);
        });

        this.handleCollapseRemoveButton();
      })
      .catch(error => {
        console.log(error);
      });
  }


  constructor() {
    try {
      this.getElements();

      this.initModalFieldElements();

      this.getStageList();

      this.handleAddButton();
      this.handleModalConfirmButton();
      this.handleModalCloseEvent();
    } catch (err) {
      throw new Error(err.message)
    }
  }
}
