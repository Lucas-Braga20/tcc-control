const FinalWorkEditor = () => {
  let menteesSelectElement = null;


  function getElements() {
    menteesSelectElement = $('[name="mentees"]');
  }

  function handleMenteesSelectElement() {
    $(menteesSelectElement).on('select2:unselecting', e => {
      const currentUser = $('[name="current-user"]').val();
    
      const userWillBeRemoved = e.params.args.data.id;
    
      if (currentUser === userWillBeRemoved) {
        e.preventDefault();
      }
    });
    
    $(menteesSelectElement).on('select2:selecting', e => {
      const selectedItems = $('[name="mentees"]').select2('val');
    
      if (selectedItems.length > 1) {
        e.preventDefault();
      }
    });
  }


  getElements();
  handleMenteesSelectElement();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkEditor();
});
