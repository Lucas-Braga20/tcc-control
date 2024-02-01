const FinalWorkStageList = () => {
  const API = {
    works: {
      updateTitle(id, title) {
        return fetch(`/tcc/api/final-works/${id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            title,
          }),
        });
      },

      updateAbleToPresent(id, ableToPresent) {
        return fetch(`/tcc/api/final-works/${id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            able_to_present: ableToPresent,
          }),
        });
      },

      updateGradingScore(id, gradingScore) {
        return fetch(`/tcc/api/final-works/${id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            grading_score: gradingScore,
          }),
        });
      },

      generateDocument(id) {
        return fetch(`/tcc/api/final-works/${id}/generate-document/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },

      documents(id) {
        return fetch(`/tcc/api/final-works/${id}/documents/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
    },
  };

  function fileNameFromPath(value) {
    try {
        return value.split('/').pop();
    } catch (error) {
        return '';
    }
  }

  function fileIcon(value) {
    try {
        const extension = value.split('.').pop().toLowerCase();

        const iconMapping = {
            'pdf': 'far fa-file-pdf',
            'txt': 'far fa-file-alt',
            'jpg': 'far fa-file-image',
            'png': 'far fa-file-image',
            'doc': 'far fa-file-word',
            'docx': 'far fa-file-word',
        };

        return iconMapping[extension] || 'far fa-file';
    } catch (error) {
        return 'far fa-file';
    }
  }

  function handleGradingScoreRange() {
    $('#tcc_grading_score_range').on('input', function (e) {
      $('#tcc_grading_score').text(this.value);
    });
  }

  function handleGradingScoreSave() {
    const setLoading = () => {
      $('#tcc_grading_score_range').addClass('disabled');
      $(this).addClass('disabled');
    }

    const removeLoading = () => {
      $('#tcc_grading_score_range').removeClass('disabled');
      $(this).removeClass('disabled');
    }

    $('#tcc_grading_score_save').click(function (e) {
      const id = $('#tcc_grading_score_container').data('final-work');

      setLoading();

      API.works.updateGradingScore(id, $('#tcc_grading_score_range').val())
        .then(response => {
          if (response.ok === false) {
            throw new Error(response.statusText);
          }
  
          return response.json();
        })
        .then(() => {
          Toast.fire({
            icon: 'success',
            title: 'TCC atualizado com sucesso.'
          });

          $('#tcc_short_grading_score').text($('#tcc_grading_score_range').val());
        })
        .catch(err => {
          Toast.fire({
            icon: 'error',
            title: 'Houve um erro no servidor.'
          });
        }).finally(() => {
          removeLoading();
        });
    });
  }

  function handleAbleToPresentButtons() {
    const setLoading = () => {
      $('.able-to-present-icons').addClass('disabled');
      $('[name="tcc_able_to_present"]').addClass('disabled');
    }

    const removeLoading = () => {
      $('.able-to-present-icons').removeClass('disabled');
      $('[name="tcc_able_to_present"]').removeClass('disabled');
    }

    $('[name="tcc_able_to_present"]').click(function(e) {
      if ($(this).hasClass('custom-disabled')) {
        e.preventDefault();
        return;
      }

      let value = $(this).val();

      if (value === 'null') {
        value = null
      } else {
        value = value === 'true'
      }

      const id = $('#tcc_able_to_present_container').data('final-work');

      setLoading();

      API.works.updateAbleToPresent(id, value).then(response => {
        if (response.ok === false) {
          throw new Error(response.statusText);
        }

        return response.json();
      }).then(() => {
        Toast.fire({
          icon: 'success',
          title: 'TCC atualizado com sucesso.'
        });

        $('#tcc_able_to_present_container').attr('data-default', String(value));

        if (value === true) {
          $('#tcc_short_able_to_present_container #tcc_short_able_to_present').text('Apto');
        } else if (value === false) {
          $('#tcc_short_able_to_present_container #tcc_short_able_to_present').text('Inapto');
        } else {
          $('#tcc_short_able_to_present_container #tcc_short_able_to_present').text('--');
        }
      }).catch(err => {
        Toast.fire({
          icon: 'error',
          title: 'Houve um erro no servidor.'
        });

        $('[name="tcc_able_to_present"]:checked').prop('checked', false);
        $(`[name="tcc_able_to_present"][value="${String($('#tcc_able_to_present_container').data('default'))}"]`).prop('checked', true);
      }).finally(() => {
        removeLoading();
      });
    });
  }

  function handleGenerateDocumentEvent() {
    $('#tcc_generate_document').click(function (e) {
      const addLoading = () => {
        $(this).html(`
          <div class="spinner-border spinner-border-sm text-gray-700 me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          Gerar Documento
        `);
        $(this).addClass('disabled');

        $('#tcc_documents_container').html(`
          <div class="d-flex justify-content-center align-items-center py-3">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <span class="ms-3">Carregando documentos...</span>
          </div>
        `);
      }

      const removeLoading = () => {
        $(this).html(`
          <span class="svg-icon svg-icon-1">
            <i class="fas fa-file-pdf fs-4"></i>
          </span>
          Gerar Documento
        `);
        $(this).removeClass('disabled');
      }

      addLoading();

      API.works.generateDocument($(this).data('tcc'))
        .then(response => response.json())
        .then(response => {
          if (response.detail != null) {
            throw new Error('Generate document error.');
          }

          return API.works.documents($(this).data('tcc'))
        })
        .then(response => response.json())
        .then(response => {
          $('#tcc_documents_container').html('');

          for (const document of response.documents) {
            $('#tcc_documents_container').append(`
              <a href="/${document.path}" class="document-file" target="_blank">
                <div class="d-flex justify-content-between border border-dashed rounded border-hover-primary border-gray-400 px-5 py-3 w-100">
                  <div class="d-flex align-items-center">
                    <span>
                      <i class="${fileIcon(document.path)} file-icon text-gray-500 fs-2"></i>
                    </span>

                    <span class="file-name fw-light text-gray-700 fs-6 ms-2">
                      ${fileNameFromPath(document.path)}
                    </span>
                  </div>

                  <span class="file-name fw-light text-gray-700 fs-6 ms-2">
                    ${document.creation_time}
                  </span>
                </div>
              </a>
            `);
          }

          if (response.documents.length === 0) {
            $('#tcc_documents_container').html(`
              <div class="border border-gray-300 rounded p-2">
                <div class="d-flex align-items-center justify-content-between p-4">
                  <h3 class="fs-7 fw-light text-gray-700 mb-0 py-1">
                    Nenhum documento foi gerado ainda.
                  </h3>
                </div>
              </div>
            `);
          }

          Toast.fire({
            icon: 'success',
            title: 'O documento foi gerado com sucesso.'
          });
        })
        .catch((err) => {
          Toast.fire({
            icon: 'error',
            title: 'Houve um erro ao gerar o documento.'
          });

          $('#tcc_documents_container').html(`
            <div class="border border-gray-300 rounded p-2">
              <div class="d-flex align-items-center justify-content-between p-4">
                <h3 class="fs-7 fw-light text-gray-700 mb-0 py-1">
                  Houve um erro ao buscar os documentos.
                </h3>
              </div>
            </div>
          `);
        })
        .finally(() => {
          removeLoading();
        });
    });
  }

  function handleUpdateTitleSection() {
    function handleSubmitEvent() {
      $('#tcc_update_title_form').submit(function (e) {
        e.preventDefault();
      });
    }

    function handleFormValidator() {
      $('#tcc_update_title_form').validate({
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
        },
        messages: {
          title: {
            required: 'O título deve ser inserido.',
            minlength: 'O título deve ter pelo menos 3 caracteres.',
            maxlength: 'O título não pode ter mais de 128 caracteres.'
          },
        },
        errorPlacement(error, element) {
          element.parent().append(error);
        },
      });
  
      $('#id_title').keyup(function(e) {
        $(this).valid();
      });
    }

    function handleMaxLengthBadge() { 
      $('#id_title').maxlength({
        warningClass: "badge badge-warning",
        limitReachedClass: "badge badge-success"
      });
    }

    function addLoading() {
      $('#id_title').addClass('disabled');
      $('#id_title').attr('disabled', true);

      $('#tcc_update_title_save').addClass('disabled');
      $('#tcc_update_title_save').attr('disabled', true);
      $('#tcc_update_title_save').html(`
        <div class="spinner-border spinner-border-sm text-white me-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        Salvar
      `);
    }

    function removeLoading() {
      $('#id_title').removeClass('disabled');
      $('#id_title').removeAttr('disabled');

      $('#tcc_update_title_save').removeClass('disabled');
      $('#tcc_update_title_save').removeAttr('disabled');
      $('#tcc_update_title_save').html(`
        Salvar
      `);
    }

    function handleSaveEvent() {
      $('#tcc_update_title_save').click(function (e) {
        const isValid = $('#tcc_update_title_form').valid();

        if (!isValid) {
          return;
        }

        addLoading();

        let fetchResponse;

        API.works.updateTitle(
          $('#tcc_update_title_container').data('tcc'),
          $('#id_title').val(),
        )
          .then(response => {
            fetchResponse = response;
            return response.json();
          })
          .then(response => {
            if (fetchResponse.ok === false) {
              let error = 'Houve um erro ao atualizar o título';

              if (response.title) {
                error = response.title[0];
              }

              if (response.detail) {
                error = response.detail[0];
              }

              Toast.fire({
                icon: 'error',
                title: error,
              });
            } else {
              $('#tcc_title').text($('#id_title').val());

              Toast.fire({
                icon: 'success',
                title: 'Título atualizado com sucesso.',
              });

              $('#tcc_update_title_container').removeClass('show');
            }
          })
          .catch(() => {
            Toast.fire({
              icon: 'error',
              title: 'Houve um erro ao atualizar o título.',
            });
          })
          .finally(() => {
            removeLoading();
          });
      });
    }

    handleSubmitEvent();
    handleFormValidator();
    handleMaxLengthBadge();
    handleSaveEvent();
  }

  handleAbleToPresentButtons();
  handleGradingScoreRange();
  handleGradingScoreSave();
  handleGenerateDocumentEvent();
  handleUpdateTitleSection();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkStageList();
});
