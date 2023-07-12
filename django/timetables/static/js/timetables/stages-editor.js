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
        const timetable = $('#tcc_stage_editor_container').data('timetable');

        return fetch(`/api/stages/?no_page=true&timetable=${timetable}`, {
          method: 'get',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      create(body) {
        return fetch(`/api/stages/`, {
          method: 'post',
          body,
          headers: {
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      delete(id) {
        return fetch(`/api/stages/${id}/`, {
          method: 'delete',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      update(body, id) {
        return fetch(`/api/stages/${id}/`, {
          method: 'patch',
          body,
          headers: {
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
    },
  };

  emptyElement = `
    <div class="accordion-item">
      <h2 class="accordion-header">
        <button
          class="accordion-button empty-item fs-4 fw-bold d-flex justify-content-center collapsed"
          type="button">
          Sem etapas.
        </button>
      </h2>
    </div>
  `;


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
          class="form-control form-control-solid tcc_start_date_field"
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
          class="form-control form-control-solid tcc_supervisor_date_field"
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
          class="form-control form-control-solid tcc_send_date_field"
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
          class="form-control form-control-solid tcc_presentation_date_field"
          placeholder="dd/mm/aaaa"
          id="${elementId}"/>
      </div>
    `;
  }

  generateStageExamplesElement(id, stage) {
    const repeaterElementId = `tcc_stage_examples_repeater_${id}`;

    let rows = '';

    stage.examples.forEach(() => {
      rows += `
        <div data-repeater-item class="mb-2">
          <div class="row g-3 align-items-center">
            <div class="tcc_create_stage_examples_link">
            </div>
            <div class="col mt-0">
              <input type="file" class="form-control form-control-solid tcc_create_stage_examples_${id}" />
            </div>
            <div class="col-auto">
              <input data-repeater-delete type="button" class="btn btn-danger" value="Remover"/>
            </div>
          </div>
        </div>
      `;
    });

    if (stage.examples.length === 0) {
      rows = `
        <div data-repeater-item class="mb-2">
          <div class="row g-3 align-items-center">
            <div class="tcc_create_stage_examples_link">
            </div>
            <div class="col mt-0">
              <input type="file" class="form-control form-control-solid tcc_create_stage_examples_${id}" />
            </div>
            <div class="col-auto">
              <input data-repeater-delete type="button" class="btn btn-danger" value="Remover"/>
            </div>
          </div>
        </div>
      `;
    }

    return `
      <div class="fv-row mb-8">
        <label class="form-label">Modelos de exemplo</label>
        <div class="fv-row" id="${repeaterElementId}">
          <div data-repeater-list="stage-examples">
            ${rows}
          </div>
          <input data-repeater-create type="button" class="btn btn-primary btn-sm" value="Adicionar"/>
        </div>
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
      defaultDate: getFlatpickrFormat(stage.start_date),
    });

    $(`#tcc_stage_editor_supervisor_date_${stage.id}`).flatpickr({
      dateFormat: 'd/m/Y',
      defaultDate: getFlatpickrFormat(stage.send_date_supervisor),
    });

    $(`#tcc_stage_editor_send_date_${stage.id}`).flatpickr({
      dateFormat: 'd/m/Y',
      defaultDate: getFlatpickrFormat(stage.send_date),
    });

    $(`#tcc_stage_editor_presentation_date_${stage.id}`).flatpickr({
      dateFormat: 'd/m/Y',
      defaultDate: getFlatpickrFormat(stage.presentation_date),
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
            ${this.generateStageExamplesElement(stage.id, stage)}

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

      let formData = new FormData();
      formData.append('description', $('#tcc_stage_editor_description').val());
      formData.append('activity_configuration', $('#tcc_stage_editor_activity').val());
      formData.append('start_date', getDatetimeFormat($('#tcc_stage_editor_start_date').val()));
      formData.append('send_date_supervisor', getDatetimeFormat($('#tcc_stage_editor_supervisor_date').val()));
      formData.append('send_date', getDatetimeFormat($('#tcc_stage_editor_send_date').val()));
      formData.append('timetable', $(ctx.container).data('timetable'));

      if ($('#tcc_stage_editor_presentation_date').val()) {
        formData.append('presentation_date', getDatetimeFormat($('#tcc_stage_editor_presentation_date').val()));
      }

      $('.tcc_create_stage_examples').each(function(index, element) {
        const files = $(element)[0].files;

        for (let i = 0; i < files.length; i++) {
          formData.append('examples', files[i]);
        }
      });

      this.API.stages.create(formData)
        .then(response => fetchResponse = response)
        .then(response => response.json())
        .then(data => {
          if (fetchResponse.status >= 300) {
            ctx.resetModalFormError();
            ctx.handleModalFormError(data);
          } else {
            ctx.getStageList();
            ctx.modal.object.hide();
            Toast.fire({
              icon: 'success',
              title: 'Etapa criada com sucesso.'
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

    if (data.examples) {
      this.addErrorInField(data.examples, `.tcc_stage_examples_repeater`);
    }
  }

  handleModalFormRepeater() {
    $('.tcc_stage_examples_repeater').repeater({
      show: function () {
        $(this).slideDown();
      },
    });
  }

  handleCollapseFormRepeater(stage) {
    $(`#tcc_stage_examples_repeater_${stage.id}`).repeater({
      show: function () {
        $(this).slideDown();
      },
    });

    $(`#tcc_stage_examples_repeater_${stage.id}`).find('[data-repeater-item]').each(function(index) {
      if (stage.examples[index]) {
        $(this).find('.tcc_create_stage_examples_link').html(`
          <span class="fw-bold">
            Arquivo atual:
            <span class="fw-light">
              <a href="${stage.examples[index].file}">
                ${extractFileNameFromURL(stage.examples[index].file)}
              </a>
            </span>
          </span>
        `);

        $(this).find(`.tcc_create_stage_examples_${stage.id}`).data('stage-example', stage.examples[index].id);
      }
    });
  }

  handleCollapseFormError(data, id) {
    if (data.description) {
      this.addErrorInField(data.description, `#tcc_stage_editor_description_${id}`);
    }

    if (data.activity_configuration) {
      this.addErrorInField(data.activity_configuration, `#tcc_stage_editor_activity_${id}`);
    }

    if (data.start_date) {
      this.addErrorInField(data.start_date, `#tcc_stage_editor_start_date${id}`);
    }

    if (data.send_date_supervisor) {
      this.addErrorInField(data.send_date_supervisor, `#tcc_stage_editor_supervisor_date${id}`);
    }

    if (data.send_date) {
      this.addErrorInField(data.send_date, `#tcc_stage_editor_send_date${id}`);
    }

    if (data.presentation_date) {
      this.addErrorInField(data.presentation_date, `#tcc_stage_editor_presentation_date${id}`);
    }

    if (data.examples) {
      this.addErrorInField(data.examples, `#tcc_stage_examples_repeater_${id}`);
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

  addLoadingStateInField(el) {
    $(el).addClass('disabled');
    $(el).attr('disabled', true);
  }

  removeLoadingStateInField(el) {
    $(el).removeClass('disabled');
    $(el).removeAttr('disabled', true);
  }

  resetModalFormError() {
    this.removeErrorInField('#tcc_stage_editor_description');
    this.removeErrorInField('#tcc_stage_editor_activity');
    this.removeErrorInField('#tcc_stage_editor_start_date');
    this.removeErrorInField('#tcc_stage_editor_supervisor_date');
    this.removeErrorInField('#tcc_stage_editor_send_date');
    this.removeErrorInField('#tcc_stage_editor_presentation_date');
    this.removeErrorInField('.tcc_stage_examples_repeater');
  }

  resetCollapseFormError(id) {
    this.removeErrorInField(`#tcc_stage_editor_description${id}`);
    this.removeErrorInField(`#tcc_stage_editor_activity${id}`);
    this.removeErrorInField(`#tcc_stage_editor_start_date${id}`);
    this.removeErrorInField(`#tcc_stage_editor_supervisor_date${id}`);
    this.removeErrorInField(`#tcc_stage_editor_send_date_${id}`);
    this.removeErrorInField(`#tcc_stage_editor_presentation_date${id}`);
    this.removeErrorInField(`#tcc_stage_examples_repeater_${id}`);
  }

  resetModalFormValues() {
    $('#tcc_stage_editor_description').val('');
    $('#tcc_stage_editor_activity').val(null).trigger('change');
    $('#tcc_stage_editor_start_date').get(0)._flatpickr.clear();
    $('#tcc_stage_editor_supervisor_date').get(0)._flatpickr.clear();
    $('#tcc_stage_editor_send_date').get(0)._flatpickr.clear();
    $('#tcc_stage_editor_presentation_date').get(0)._flatpickr.clear();

    $('.tcc_stage_examples_repeater [data-repeater-item]').slice(1).empty();
    $('.tcc_stage_examples_repeater [data-repeater-item] .tcc_create_stage_examples').val('');
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
          let fetchResponse;

          ctx.API.stages.delete($(this).data('id'))
            .then(response => fetchResponse = response)
            .then(response => {
              return response.json().catch(() => {
                throw new Error('Houve um erro no servidor.');
              })
            })
            .then(response => {
              if (fetchResponse.status >= 300) {
                throw new Error(response.detail || 'Houve um erro no servidor.');
              } else {
                Toast.fire({
                  icon: 'success',
                  title: 'Etapa removida com sucesso.'
                });
  
                ctx.getStageList();
              }
            })
            .catch(err => {
              Toast.fire({
                icon: 'error',
                title: err.message,
              });
            });
        }
      });
    });
  }

  handleCollapseSaveButton() {
    const ctx = this;

    $('.tcc_save_button').click(function (e) {
      const accordion = $(this).parent().parent().parent();

      ctx.addLoadingStateInField($(accordion).find('.tcc_description_field'));
      ctx.addLoadingStateInField($(accordion).find('.tcc_activity_field'));
      ctx.addLoadingStateInField($(accordion).find('.tcc_start_date_field'));
      ctx.addLoadingStateInField($(accordion).find('.tcc_supervisor_date_field'));
      ctx.addLoadingStateInField($(accordion).find('.tcc_send_date_field'));
      ctx.addLoadingStateInField($(accordion).find('.tcc_presentation_date_field'));

      const id = $(this).data('id');

      let fetchResponse;

      let formData = new FormData();
      formData.append('description', $(accordion).find('.tcc_description_field').val());
      formData.append('activity_configuration', $(accordion).find('.tcc_activity_field').val());
      formData.append('start_date', getDatetimeFormat($(accordion).find('.tcc_start_date_field').val()));
      formData.append('send_date_supervisor', getDatetimeFormat($(accordion).find('.tcc_supervisor_date_field').val()));
      formData.append('send_date', getDatetimeFormat($(accordion).find('.tcc_send_date_field').val()));
      formData.append('timetable', $(ctx.container).data('timetable'));

      if ($(accordion).find('.tcc_presentation_date_field').val()) {
        formData.append('presentation_date', getDatetimeFormat($(accordion).find('.tcc_presentation_date_field').val()));
      }

      $(`.tcc_create_stage_examples_${id}`).each(function(index, element) {
        const data = $(element).data('stage-example');

        if (data) {
          formData.append('already_uploaded', data);
        } else {
          const files = $(element)[0].files;

          for (let i = 0; i < files.length; i++) {
            formData.append('examples', files[i]);
          }
        }
      });

      ctx.API.stages.update(formData, $(this).data('id'))
        .then(response => fetchResponse = response)
        .then(response => response.json())
        .then(data => {
          if (fetchResponse.status >= 300) {
            ctx.resetCollapseFormError($(this).data('id'));
            ctx.handleCollapseFormError(data, $(this).data('id'));
          } else {
            ctx.getStageList();
            Toast.fire({
              icon: 'success',
              title: 'Etapa atualizada com sucesso.'
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
          ctx.removeLoadingStateInField($(accordion).find('.tcc_description_field'));
          ctx.removeLoadingStateInField($(accordion).find('.tcc_activity_field'));
          ctx.removeLoadingStateInField($(accordion).find('.tcc_start_date_field'));
          ctx.removeLoadingStateInField($(accordion).find('.tcc_supervisor_date_field'));
          ctx.removeLoadingStateInField($(accordion).find('.tcc_send_date_field'));
          ctx.removeLoadingStateInField($(accordion).find('.tcc_presentation_date_field'));
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

        if (response && response.length > 0) {
          response.forEach(stage => {
            this.addItemElementToList(stage);
            this.handleCollapseFormRepeater(stage);
          });
        } else {
          $(this.container).html(this.emptyElement);
        }

        this.handleCollapseRemoveButton();
        this.handleCollapseSaveButton();
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
      this.handleModalFormRepeater();
    } catch (err) {
      throw new Error(err.message)
    }
  }
}
