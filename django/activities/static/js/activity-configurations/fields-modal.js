class ActivityFieldsEditor {
  container = null;

  addButton = null;

  // Modal
  modal = {
    element: null,
    object: null,
    confirmButton: null,
  };

  formFieldsElements = {
    name: null,
    type: null,
    key: null,
  };

  inputElement = null;
  items = new Array();

  loadingElement = `
    <div class="d-flex justify-content-center align-items-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <span class="ms-3">Carregando campos...</span>
    </div>
  `
  emptyElement = `
    <div class="accordion-item">
      <h2 class="accordion-header">
        <button
          class="accordion-button empty-item fs-4 fw-bold d-flex justify-content-center collapsed"
          type="button">
          Sem campos.
        </button>
      </h2>
    </div>
  `;

  removeItem(index) {
    if (index > -1) {
      this.items.splice(index, 1);
    }
  }

  updateItem(index, value) {
    if (index > -1) {
      this.items[index] = {
        id: value.id,
        name: value.name,
        type: value.type,
        key: value.key,
      };
    }
  }


  // Fields Validation
  validateNameField(value, element) {
    const hasErrors = $(element).hasClass('is-invalid');

    if (value.length === 0) {
      if (!hasErrors) {
        $(element).addClass('is-invalid');
        $(element).parent().append(`
          <div class="invalid-feedback">
            O campo nome é obrigatório.
          </div>
        `);
      }
    } else {
      $(element).removeClass('is-invalid');
      let feedbacks = $(element).parent().find('.invalid-feedback');

      if (feedbacks != null) {
        feedbacks.remove();
      }
    }
  }
  handleNameFields() {
    const ctx = this;

    $('.tcc_name_field').keyup(function (e) {
      ctx.validateNameField($(this).val(), $(this));
    });
  }

  validateKeyField(value, element) {
    const hasErrors = $(element).hasClass('is-invalid');

    if (value.length === 0) {
      if (!hasErrors) {
        $(element).addClass('is-invalid');
        $(element).parent().append(`
          <div class="invalid-feedback">
            O campo chave é obrigatório.
          </div>
        `);
      }
    } else {
      $(element).removeClass('is-invalid');
      let feedbacks = $(element).parent().find('.invalid-feedback');

      if (feedbacks != null) {
        feedbacks.remove();
      }
    }
  }
  handleKeyFields() {
    const ctx = this;

    $('.tcc_key_field').keyup(function (e) {
      ctx.validateKeyField($(this).val(), $(this));
    });
  }

  getIsValidForm(name, type, key) {
    return !((name == null || name == '') || (type == null) || (key == null || key == ''));
  }


  // Reset form values.
  resetForm() {
    $(this.formFieldsElements.name).val('');
    $(this.formFieldsElements.key).val('');
  }


  // Manipulate elements in list.
  addItemElementToList(name, type, key, id) {
    const nameField = $(this.formFieldsElements.name).parent().clone();
    nameField.find('input').attr('id', `tcc_fields_editor_update_name_${id}`);

    const typeField = $(this.formFieldsElements.type).parent().clone();
    typeField.find('select').attr('id', `tcc_fields_editor_update_type_${id}`);

    const keyField = $(this.formFieldsElements.key).parent().clone();
    keyField.find('input').attr('id', `tcc_fields_editor_update_key_${id}`);

    const element = `
      <div id="tcc_accordion-item_${id}" class="accordion-item">
        <h2 class="accordion-header" id="tcc_accordion_header_${id}">
          <button
            class="accordion-button fs-4 fw-bold collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#tcc_accordion_body_${id}"
            aria-expanded="true"
            aria-controls="tcc_accordion_body_${id}">
            <div class="d-flex justify-content-between w-100">
              <div>
                ${name}
              </div>
              <div>
                ${key}
              </div>
              <div class="me-3">
                ${type}
              </div>
            </div>
          </button>
        </h2>
        <div
          id="tcc_accordion_body_${id}"
          class="accordion-collapse collapse"
          aria-labelledby="tcc_accordion_body_${id}"
          data-bs-parent="#tcc_accordion_body_${id}">
          <div class="accordion-body">
            ${nameField.get(0).outerHTML}
            ${typeField.get(0).outerHTML}
            ${keyField.get(0).outerHTML}

            <div class="d-flex justify-content-end mt-8">
              <div>
                <button type="button" class="btn btn-sm btn-danger tcc_remove_button" data-id="${id}">Remover</button>
              </div>
              <div class="ms-2">
                <button type="button" class="btn btn-sm btn-primary tcc_save_button" data-id="${id}">Salvar</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    if (this.items.length === 0) {
      $(this.container).html(element);
    } else {
      $(this.container).append(element);
    }

    $(`#tcc_fields_editor_update_name_${id}`).val(name)
    $(`#tcc_fields_editor_update_type_${id}`).val(type)
    $(`#tcc_fields_editor_update_key_${id}`).val(key)

    this.handleNameFields();
    this.handleKeyFields();

    this.handleRemoveButtons();
    this.handleSaveButtons();
  }

  removeItemElementInList(id) {
    $(`#tcc_accordion-item_${id}`).remove();

    if (this.items.length === 0) {
      $(this.container).html(this.emptyElement);
    }
  }

  updateItemElementInList(value) {
    $(`#tcc_accordion-item_${value.id}`).find('.accordion-button').html(`
      <div class="d-flex justify-content-between w-100">
        <div>
          ${value.name}
        </div>
        <div>
          ${value.key}
        </div>
        <div class="me-3">
          ${value.type}
        </div>
      </div>
    `);
  }

  loadItensElements(initial) {
    initial.forEach(value => {
      const id = Date.now();

      this.addItemElementToList(value.name, value.type, value.key, id);

      this.items.push({
        id,
        name: {
          value: value.name,
          element: document.getElementById(`tcc_fields_editor_update_name_${id}`),
        },
        type: {
          value: value.type,
          element: document.getElementById(`tcc_fields_editor_update_type_${id}`),
        },
        key: {
          value: value.key,
          element: document.getElementById(`tcc_fields_editor_update_key_${id}`),
        },
      });
    });
  }


  // Get json response from added itens.
  getJsonFields() {
    let response = {};

    if (this.items.length !== 0) {
      response['fields'] = this.items.map(item => {
        return {
          name: item.name.value,
          type: item.type.value,
          key: item.key.value,
        }
      });
      return JSON.stringify(response);
    }

    return null;
  }


  // Modal Events
  handleAddButton() {
    $(this.addButton).click(() => {
      this.modal.object.show();
    })
  }

  handleConfirmButton() {
    $(this.modal.confirmButton).click(() => {
      let name = $(this.formFieldsElements.name).val();
      let type = $(this.formFieldsElements.type).val();
      let key = $(this.formFieldsElements.key).val();

      if (this.getIsValidForm(name, type, key)) {
        const id = Date.now();

        this.addItemElementToList(name, type, key, id);

        this.items.push({
          id: id,
          name: {
            value: name,
            element: document.getElementById(`tcc_fields_editor_update_name_${id}`),
          },
          type: {
            value: type,
            element: document.getElementById(`tcc_fields_editor_update_type_${id}`),
          },
          key: {
            value: key,
            element: document.getElementById(`tcc_fields_editor_update_key_${id}`),
          },
        });

        const response = this.getJsonFields();
        $(this.inputElement).val(response);

        this.resetForm();
        this.modal.object.hide();
      } else {
        this.validateNameField(name, this.formFieldsElements.name);
        this.validateKeyField(key, this.formFieldsElements.key);
      }
    });
  }

  handleRemoveButtons() {
    const ctx = this;

    $('.tcc_remove_button').click(function() {
      const id = $(this).data('id');

      const find = ctx.items.findIndex(item => item.id == id);

      if (find != null) {
        ctx.removeItem(find);
        ctx.removeItemElementInList(id);
        $(ctx.inputElement).val(ctx.getJsonFields());
      }
    });
  }

  handleSaveButtons() {
    const ctx = this;

    $('.tcc_save_button').click(function () {
      const id = $(this).data('id');

      const name = $(`#tcc_fields_editor_update_name_${id}`);
      const type = $(`#tcc_fields_editor_update_type_${id}`);
      const key = $(`#tcc_fields_editor_update_key_${id}`);

      if (ctx.getIsValidForm(name.val(), type.val(), key.val())) {
        const find = ctx.items.findIndex(item => item.id == id);
  
        if (find != null) {
          ctx.updateItem(find, {
            id,
            name: {
              value: name.val(),
              element: name,
            },
            type: {
              value: type.val(),
              element: type,
            },
            key: {
              value: key.val(),
              element: key,
            },
          });
          ctx.updateItemElementInList({
            id, name: name.val(), type: type.val(), key: key.val()
          });
          $(ctx.inputElement).val(ctx.getJsonFields());
        }
      }
    })
  }


  // Get HTML elements.
  getElements() {
    try {
      this.container = document.getElementById('tcc_fields_editor_container');
      this.addButton = document.getElementById('tcc_fields_editor_add_btn');
      this.formFieldsElements.name = document.getElementById('tcc_fields_editor_name');
      this.formFieldsElements.type = document.getElementById('tcc_fields_editor_type');
      this.formFieldsElements.key = document.getElementById('tcc_fields_editor_key');
      this.inputElement = document.getElementById('tcc_fields_editor');
      this.modal.confirmButton = document.getElementById('tcc_fields_editor_modal_confirm_button');
      this.modal.element = document.getElementById('tcc_modal_field');
      this.modal.object = new bootstrap.Modal(this.modal.element);

    } catch (err) {
      console.log(err)
      throw new Error('Activity Fields Editor - Cannot find elements.');
    }
  }


  constructor() {
    try {
      this.getElements();

      if ($(this.inputElement).val() != '') {
        const initialData = JSON.parse($(this.inputElement).val());
        if (initialData != null && initialData.fields != null) {
          this.loadItensElements(initialData.fields);
        }
      }

      this.handleAddButton();
      this.handleConfirmButton();

      this.handleNameFields();
      this.handleKeyFields();

      if (this.items.length === 0) {
        $(this.container).html(this.emptyElement);
      }
    } catch (err) {
      throw new Error(err.message)
    }
  }
}
