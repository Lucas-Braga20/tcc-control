const FinalWorkStageList = () => {
  const API = {
    works: {
      updateAbleToPresent(id, ableToPresent) {
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

      updateGradingScore(id, gradingScore) {
        return fetch(`/api/final-works/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            grading_score: gradingScore,
          }),
        });
      },
    },
  };

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
  handleGradingScoreRange();
  handleGradingScoreSave();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkStageList();
});
