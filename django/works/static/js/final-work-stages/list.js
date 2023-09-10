const FinalWorkStageList = () => {
  const API = {
    works: {
      update(id, ableToPresent) {
        return fetch(`/api/final-works/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            able_to_present: ableToPresent,
          }),
        });
      },
    },
  };

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

      API.works.update(id, value).then(response => {
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

  handleAbleToPresentButtons();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkStageList();
});
